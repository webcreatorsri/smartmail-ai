import streamlit as st
import os
import json
import time
from gmail_utils import get_service, get_latest_emails
from summarizer import summarize_email
from classifier import classify_email
from google.oauth2.credentials import Credentials

st.set_page_config(page_title="SmartMail AI", layout="wide")
st.title("📬 SmartMail AI - Summarized Inbox")

# ✅ Check if Gmail token file exists
if not os.path.exists("token.json"):
    st.warning("⚠️ Please log in to Gmail via [Flask Login](http://localhost:5000/login)")
    st.stop()

# ✅ Load token from file
with open("token.json", "r") as f:
    token_data = json.load(f)

# ✅ Build Gmail credentials
creds = Credentials(
    token=token_data["token"],
    refresh_token=token_data["refresh_token"],
    token_uri=token_data["token_uri"],
    client_id=token_data["client_id"],
    client_secret=token_data["client_secret"],
    scopes=token_data["scopes"],
)

# ✅ Get Gmail service
service = get_service(creds)

# ✅ Fetch latest emails
emails = get_latest_emails(service)

if not emails:
    st.info("🎉 No unread emails.")
else:
    for email in emails:
        subject = email.get("subject", "(No Subject)")
        sender = email.get("from", "(Unknown Sender)")
        body = email.get("body", "")

        # ❌ Removed the summary here to avoid duplication
        # ✅ Show details only after expanding
        with st.expander(subject):
            st.markdown(f"**From:** {sender}")
            st.markdown(f"**Summary:** {summarize_email(body)}")
            st.markdown(f"**Importance:** {classify_email(subject, sender)}")
            