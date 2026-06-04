# agent/whatsapp_sender.py
import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID  = os.getenv("TWILIO_ACCOUNT_SID")
AUTH_TOKEN   = os.getenv("TWILIO_AUTH_TOKEN")
FROM_NUMBER  = os.getenv("TWILIO_WHATSAPP_FROM")  # whatsapp:+14155238886

def send_whatsapp(to_phone, message):
    if not ACCOUNT_SID or not AUTH_TOKEN:
        print("[WhatsApp] Credentials missing in .env")
        return False, "Missing credentials"

    # Normalize: strip any existing whatsapp: prefix, re-add cleanly
    to_number = f"whatsapp:{to_phone.replace('whatsapp:', '')}"

    try:
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        msg = client.messages.create(
            body=message,
            from_=FROM_NUMBER,
            to=to_number,
        )
        print(f"[WhatsApp] ✓ Sent to {to_phone} | SID: {msg.sid}")
        return True, None
    except Exception as e:
        print(f"[WhatsApp] ✗ Failed: {e}")
        return False, str(e)