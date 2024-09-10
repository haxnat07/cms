from app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False,unique=True)
    password = db.Column(db.String(255), nullable=False)
    
