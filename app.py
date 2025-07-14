# app.py

from flask import Flask, redirect, url_for, session, request, render_template
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import os
import json
from dotenv import load_dotenv
from datetime import datetime

from models import db, Login  # ✅ Import SQLAlchemy and Login model

# ✅ Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# ✅ Configure MySQL
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("MYSQL_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# ✅ For local development only
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# ✅ OAuth Configuration
CLIENT_SECRETS_FILE = "credentials.json"
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
REDIRECT_URI = "http://localhost:5000/callback"

flow = Flow.from_client_secrets_file(
    CLIENT_SECRETS_FILE,
    scopes=SCOPES,
    redirect_uri=REDIRECT_URI
)

@app.route("/")
def index():
    return render_template("login.html")

@app.route('/login')
def login():
    authorization_url, state = flow.authorization_url(prompt='consent')
    session['state'] = state
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)
    creds = flow.credentials

    session['creds'] = {
        'token': creds.token,
        'refresh_token': creds.refresh_token,
        'token_uri': creds.token_uri,
        'client_id': creds.client_id,
        'client_secret': creds.client_secret,
        'scopes': creds.scopes
    }

    # ✅ Get email using Gmail API (safer than relying on ID token)
    try:
        gmail = build("gmail", "v1", credentials=creds)
        profile = gmail.users().getProfile(userId='me').execute()
        user_email = profile.get("emailAddress", "unknown@example.com")
    except Exception as e:
        print(f"[Gmail Profile Error] {e}")
        user_email = "unknown@example.com"

    # ✅ Save login to database
    login = Login(email=user_email)
    db.session.add(login)
    db.session.commit()

    # ✅ Save token to file for Streamlit
    with open("token.json", "w") as token_file:
        json.dump(session["creds"], token_file)

    return redirect("http://localhost:8501")

if __name__ == "__main__":
    app.run(port=5000, debug=True)
