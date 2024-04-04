from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String(150))
    email = db.Column(db.String(150))
    messages = db.Column(db.String(10000))
    user_ip = db.Column(db.String(100)) 

    def __str__(self):
        return self.name

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(255))


    def __repr__(self):
        return f'<User {self.email}>'
