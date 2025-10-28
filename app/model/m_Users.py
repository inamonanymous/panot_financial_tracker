from app.ext import db, dt

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(32), nullable=False)
    lastname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    current_value = db.Column(db.Float, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=dt.now())
    updated_at = db.Column(db.DateTime, default=dt.now()) 

