# streamlit_app.py

import streamlit as st
import os
import json
import pandas as pd
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from gmail_utils import get_service, get_latest_emails
from summarizer import summarize_email
from classifier import classify_email

from models import db, Email, Login
from app import app  # Provides app context

# 🔧 Streamlit Page Settings
st.set_page_config(page_title="SmartMail AI", layout="wide")
st.title("📬 SmartMail AI")

# Initialize session state
if "view" not in st.session_state:
    st.session_state.view = None
if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

# 🔘 UI for Navigation
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("📥 Login to see Mails"):
        st.session_state.view = "user"
        st.markdown("""
            <meta http-equiv="refresh" content="0;url=http://localhost:5000/login" />
        """, unsafe_allow_html=True)

with col2:
    if st.button("🔐 Admin View"):
        st.session_state.view = "admin"

# Step 4: Gmail Inbox after Flask login
if os.path.exists("token.json"):
    if st.session_state.view != "user":
        st.session_state.view = "user"

if st.session_state.view == "user" and os.path.exists("token.json"):
    st.subheader("📨 Summarized Inbox")

    with open("token.json", "r") as f:
        token_data = json.load(f)

    creds = Credentials(
        token=token_data["token"],
        refresh_token=token_data["refresh_token"],
        token_uri=token_data["token_uri"],
        client_id=token_data["client_id"],
        client_secret=token_data["client_secret"],
        scopes=token_data["scopes"],
    )

    try:
        service = get_service(creds)
        profile = service.users().getProfile(userId='me').execute()
        profile_email = profile.get("emailAddress", "unknown@example.com")

        emails = get_latest_emails(service)

        if not emails:
            st.info("🎉 No unread emails.")
        else:
            for email in emails:
                gmail_id = email.get("gmail_id")
                subject = email.get("subject", "(No Subject)")
                sender = email.get("from", "(Unknown Sender)")
                body = email.get("body", "")
                received_at = datetime.fromtimestamp(email.get("received_at", 0))
                summary = summarize_email(body)
                importance = classify_email(subject, sender)

                with st.expander(subject):
                    st.markdown(f"**From:** {sender}")
                    st.markdown(f"**Summary:** {summary}")
                    st.markdown(f"**Importance:** {importance}")

                with app.app_context():
                    if not Email.query.filter_by(gmail_id=gmail_id).first():
                        record = Email(
                            gmail_id=gmail_id,
                            user_email=profile_email,
                            subject=subject,
                            sender=sender,
                            summary=summary,
                            importance=importance,
                            received_at=received_at
                        )
                        db.session.add(record)
                        db.session.commit()

        if st.button("🚪 Logout Gmail"):
            os.remove("token.json")
            st.session_state.view = None
            st.rerun()

    except Exception as e:
        st.error(f"❌ Gmail access error: {e}")
        if st.button("Try Logging in Again"):
            st.markdown('<meta http-equiv="refresh" content="0; url=http://localhost:5000/login" />', unsafe_allow_html=True)

# ============================
# 🔐 Admin Login + View Mode
# ============================
if st.session_state.view == "admin" and not st.session_state.admin_logged_in:
    st.subheader("🔐 Admin Login")
    with st.form("admin_login_form"):
        email = st.text_input("Admin Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if email == "jayasrip1808@gmail.com" and password == "jg17181718":
                st.session_state.admin_logged_in = True
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

elif st.session_state.view == "admin" and st.session_state.admin_logged_in:
    st.sidebar.subheader("📌 Filter Emails by Importance")
    importance_filter = st.sidebar.radio("Importance", ["All", "✅ Important", "❌ Not Important"])

    st.subheader("📥 Stored Emails")

    with app.app_context():
        emails = Email.query.order_by(Email.received_at.desc()).all()

    email_data = [{
        "Email": e.user_email,
        "Subject": e.subject,
        "Sender": e.sender,
        "Summary": e.summary,
        "Importance": e.importance,
        "Received At": e.received_at.strftime("%Y-%m-%d %H:%M:%S")
    } for e in emails]

    df = pd.DataFrame(email_data)

    if importance_filter != "All":
        df = df[df["Importance"] == importance_filter]

    st.dataframe(df, use_container_width=True)
    st.success(f"📧 Total Emails: {len(df)}")
    st.download_button("⬇️ Download Emails", df.to_csv(index=False).encode(), "emails.csv", "text/csv")

    st.markdown("---")
    st.subheader("👥 Login History")

    with app.app_context():
        logins = Login.query.order_by(Login.login_time.desc()).all()

    login_df = pd.DataFrame([{
        "Email": l.email,
        "Login Time": l.login_time.strftime("%Y-%m-%d %H:%M:%S")
    } for l in logins])

    st.dataframe(login_df, use_container_width=True)
    st.success(f"👤 Total Logins: {len(login_df)}")
    st.download_button("⬇️ Download Login History", login_df.to_csv(index=False).encode(), "login_history.csv", "text/csv")

    if st.button("🚪 Logout Admin"):
        st.session_state.admin_logged_in = False
        st.session_state.view = None
        st.rerun()
