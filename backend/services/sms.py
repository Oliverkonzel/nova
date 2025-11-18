"""
SMS Service - Sends text messages via Twilio
"""
from twilio.rest import Client
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_confirmation_sms(to_phone: str, name: str, appointment_time: str) -> bool:
    """Send appointment confirmation via SMS"""
    try:
        message_body = f"""Hi {name}! 

Your free consultation with Orbyn.ai is confirmed for {appointment_time}.

We'll call you at this number. Looking forward to speaking with you!

- The Orbyn.ai Team"""

        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        
        print(f"✅ SMS sent! SID: {message.sid}")
        return True
        
    except Exception as e:
        print(f"❌ SMS error: {e}")
        return False

def send_simple_sms(to_phone: str, message: str) -> bool:
    """Send a simple SMS message"""
    try:
        msg = twilio_client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=to_phone
        )
        
        print(f"✅ SMS sent! SID: {msg.sid}")
        return True
        
    except Exception as e:
        print(f"❌ SMS error: {e}")
        return False
