from base64 import decode
import email
import bcrypt
from flask import Flask, jsonify, request
from database import db
from model.User import User
from model.Snack import Snack
from flask_login import LoginManager, login_user
from bcrypt import checkpw, hashpw

app = Flask(__name__)
login_manager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
login_manager.login_view = 'login'

db.init_app(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and checkpw(password.encode(),user.password):
        login_user(user)
        return jsonify({'message':'Login successful'}),200
    
    return jsonify({'message':'Invalid email or password'}),401

@app.route('/register',methods=['POST'])
def register():
    data = request.get_json()
 
    if not all([data.get('name'), data.get('email'), data.get('password')]):
        return jsonify({'message':'Missing required fields'}),400

    user_exists = User.query.filter_by(email=data['email']).first()

    if user_exists:
        return jsonify({"message":"Email is already in use."}), 400
    
    password_hash = hashpw(str.encode(data['password']),bcrypt.gensalt())

    user = User(name=data['name'],email=data['email'],password=password_hash)
    db.session.add(user)
    db.session.commit()
   
    return jsonify({
        "message":"User created successful",
        "user": user.to_dict()
    }), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)