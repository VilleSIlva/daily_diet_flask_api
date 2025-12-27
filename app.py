from flask import Flask
from database import db
from model.User import User
from model.Snack import Snack
from flask_login import LoginManager, login_manager

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

if __name__ == "__main__":
    app.run(debug=True)