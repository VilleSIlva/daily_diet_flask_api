import bcrypt
from flask import Flask, jsonify, request
from database import db
from model.User import User
from model.Snack import Snack
from flask_login import LoginManager, login_required, login_user, current_user, logout_user
from bcrypt import checkpw, hashpw
from datetime import datetime

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
    data = request.get_json(silent=True)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"message":"Missing required fields"}), 400

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
    }), 201

@app.route('/logout',methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify({"message":"Logout success"})

@app.route("/snacks", methods=["POST"])
@login_required
def create_snacks():
    data = request.get_json()

    if not all([data.get('name'),data.get('description'), data.get('diet_date')]):
        return jsonify({"message":"Missing required fields"}), 400

    try:
        diet_date = datetime.fromisoformat(data.get('diet_date'))
    except ValueError:
        return jsonify({"message":"Invalid date"}), 400

    snack = Snack(
        name=data['name'],
        description=data['description'],
        diet=data.get('diet',False),
        diet_date= diet_date,
        user_id=current_user.id
    )

    db.session.add(snack)
    db.session.commit()

    return jsonify({
        "message":"Snack created sucessful",
        "snack":snack.to_dict()
    })

@app.route("/snacks",methods=["GET"])
@login_required
def get_snack():
    
    snacks = Snack.query.filter_by(user_id=current_user.id)

    snacks = [snack.to_dict() for snack in snacks]

    return jsonify({"snacks":snacks})

@app.route("/snacks/<int:id>",methods=["GET"])
@login_required
def get_snack(id):
    snack = Snack.query.get(id)

    if not snack:
        return jsonify({"message":"Snack not found"}), 404

    if snack.user_id != current_user.id:
        return jsonify({"message":"Unauthorized"}),403

    return jsonify({
        "snack":snack.to_dict()
    })

@app.route("/snacks/<int:id>", methods=['PUT'])
def update_snack(id):
    data = request.get_json()
    snack = Snack.query.get(id)

    if not snack:
        return jsonify({"message":"Snack not found"}), 404

    if snack.user_id != current_user.id:
        return jsonify({"message":"Unauthorized"}),403

    try:
        diet_date = data.get('diet_date')
        if diet_date:
            diet_date = datetime.fromisoformat(data.get('diet_date'))
        else:
            diet_date = snack.diet_date
    except ValueError:
        return jsonify({"message":"Invalidad date"}), 400
 
    snack.name = data.get('name',snack.name)
    snack.description = data.get('description',snack.description)
    snack.diet = data.get('diet',snack.diet)
    snack.diet_date = diet_date

    db.session.commit()

    return jsonify({
        "message":"Snack update successfully",
        "snacks": snack.to_dict()
    })


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)