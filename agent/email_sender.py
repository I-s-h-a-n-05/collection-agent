# agent/email_sender.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

GMAIL_ADDRESS      = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

def send_email(to_address, subject, body):
    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("[Email] Credentials missing in .env")
        return False, "Missing credentials"

    msg = MIMEMultipart()
    msg["From"]    = GMAIL_ADDRESS
    msg["To"]      = to_address
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_address, msg.as_string())
        print(f"[Email] ✓ Sent to {to_address}")
        return True, None
    except Exception as e:
        print(f"[Email] ✗ Failed: {e}")
        return False, str(e)