# models.py

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

db = SQLAlchemy()

def india_time():
    return datetime.utcnow() + timedelta(hours=5, minutes=30)

class Login(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    login_time = db.Column(db.DateTime, default=india_time)

class Email(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gmail_id = db.Column(db.String(100), unique=True)
    user_email = db.Column(db.String(255))
    subject = db.Column(db.Text)
    sender = db.Column(db.String(255))
    summary = db.Column(db.Text)
    importance = db.Column(db.String(50))
    received_at = db.Column(db.DateTime)