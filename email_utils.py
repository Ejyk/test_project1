# email_utils.py
import smtplib
from email.message import EmailMessage
import streamlit as st

def send_email(to, subject, message):
    EMAIL_ADDRESS = st.secrets["EMAIL_ADDRESS"]  # should be info@einstservices.com
    EMAIL_PASSWORD = st.secrets["EMAIL_PASSWORD"]  # your mailbox password

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to
    msg.set_content(message)

    # ✅ FastHosts SMTP
    with smtplib.SMTP("smtp.fasthosts.co.uk", 587) as smtp:
        smtp.set_debuglevel(1)        # optional: shows debug info in terminal
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def notify_admin(subject, message):
    admin_email = st.secrets["ADMIN_EMAIL"]
    send_email(admin_email, subject, message)
