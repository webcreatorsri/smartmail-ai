from app import app
from models import db

with app.app_context():
    db.create_all()

print("✅ Tables created in smartmail_ai database.")
