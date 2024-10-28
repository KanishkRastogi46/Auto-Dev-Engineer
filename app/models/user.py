from flask_login import UserMixin
from app import db

class User(UserMixin , db.Model):
    id = db.Column(db.String(36), primary_key=True)
    fullname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password  = db.Column(db.String(60), nullable=False)
    # profile_img = db.Column(db.String(500), nullable=True)