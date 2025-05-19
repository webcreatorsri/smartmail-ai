from flask import Flask, redirect, url_for, session, request
from google_auth_oauthlib.flow import Flow
from flask import render_template
import os
import pathlib
from dotenv import load_dotenv
import json


# Load .env
load_dotenv()


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  # dev only

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
      # Save creds to file (optional)
    with open("token.json", "w") as token_file:
        json.dump(session["creds"], token_file)

    return redirect("http://localhost:8501")  # Open Streamlit after login


if __name__ == "__main__":
    app.run(port=5000, debug=True)
