from flask import Flask, jsonify, request
from database import db
from model.User import User
from model.Snack import Snack
from flask_login import LoginManager, login_manager, login_user
from bcrypt import checkpw

app = Flask(__name__)
flask_login = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
flask_login.login_view = 'login'

db.init_app(app)
flask_login.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login',methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if user and checkpw(password.encode,user.password.encode):
        login_user(user)
        return jsonify({'message':'Login successful'}),200
    
    return jsonify({'message':'Invalid email or password'}),401

if __name__ == "__main__":
    app.run(debug=True)