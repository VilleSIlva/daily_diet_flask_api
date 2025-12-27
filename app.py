from flask import Flask
from database import db
from model.User import User
from model.Snack import Snack

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)