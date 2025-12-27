from database import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    snacks = db.relationship('Snack', backref='user', lazy=True)
