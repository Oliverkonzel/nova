"""
Configuration file - loads all API keys and settings from .env file
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Cal.com Configuration
CAL_API_KEY = os.getenv("CAL_API_KEY")
CAL_EVENT_TYPE = os.getenv("CAL_EVENT_TYPE")
CAL_API_URL = "https://api.cal.com/v1"

# Notion Configuration
NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
NOTION_API_URL = "https://api.notion.com/v1"

# Server Configuration
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# Nova's personality and instructions
NOVA_SYSTEM_PROMPT = """You are Nova, a friendly AI voice assistant for Orbyn.ai. 

Your job is to:
1. Greet callers warmly
2. Ask for their name and phone number
3. Ask what service they're interested in
4. Offer to schedule a free consultation

Keep responses SHORT and conversational - you're on a phone call.
Be professional but friendly.
Always confirm information by repeating it back.

Example:
Caller: "Hi, I'm looking for help with AI automation"
You: "Great! I'd love to help. Can I get your full name?"
Caller: "John Smith"
You: "Thanks John! And what's the best phone number to reach you?"
"""
