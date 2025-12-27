from database import db
from flask_login import UserMixin
from datetime import datetime

class User(db.Model,UserMixin):

    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    snacks = db.relationship('Snack', backref='user', lazy=True)

    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "email":self.email,
            "created_at":self.created_at
        }