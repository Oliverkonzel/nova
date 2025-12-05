"""
Conversation Service - Handles AI conversation using OpenAI
"""
from openai import OpenAI
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import OPENAI_API_KEY, NOVA_SYSTEM_PROMPT
from models import ConversationState, Message
import json

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Store active conversations
active_conversations = {}

def get_conversation(call_sid: str) -> ConversationState:
    """Get or create a conversation state for a call"""
    if call_sid not in active_conversations:
        active_conversations[call_sid] = ConversationState(call_sid=call_sid)
    return active_conversations[call_sid]

def generate_response(call_sid: str, user_message: str) -> tuple[str, dict]:
    """
    Generate Nova's response to what the user said
    
    Returns:
        tuple: (Nova's response text, extracted data)
    """
    conversation = get_conversation(call_sid)
    conversation.messages.append(Message(role="user", content=user_message))
    
    # Build messages for OpenAI
    messages = [{"role": "system", "content": NOVA_SYSTEM_PROMPT}]
    
    for msg in conversation.messages:
        messages.append({"role": msg.role, "content": msg.content})
    
    # Add extraction instructions
    messages.append({
        "role": "system", 
        "content": """After your response, output a JSON object with any extracted info:
{
  "name": "extracted name or null",
  "phone": "extracted phone or null", 
  "email": "extracted email or null",
  "service": "extracted service or null",
  "ready_to_book": true/false
}"""
    })
    
    # Call OpenAI
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,
        max_tokens=150
    )
    
    assistant_message = response.choices[0].message.content
    conversation.messages.append(Message(role="assistant", content=assistant_message))
    
    # Extract structured data
    extracted_data = {}
    try:
        if "{" in assistant_message and "}" in assistant_message:
            json_start = assistant_message.rfind("{")
            json_end = assistant_message.rfind("}") + 1
            json_str = assistant_message[json_start:json_end]
            extracted_data = json.loads(json_str)
            
            # Update call data
            if extracted_data.get("name"):
                conversation.call_data.name = extracted_data["name"]
            if extracted_data.get("phone"):
                conversation.call_data.phone = extracted_data["phone"]
            if extracted_data.get("email"):
                conversation.call_data.email = extracted_data["email"]
            if extracted_data.get("service"):
                conversation.call_data.service = extracted_data["service"]
            
            # Remove JSON from response
            assistant_message = assistant_message[:json_start].strip()
    except:
        pass
    
    return assistant_message, extracted_data

def end_conversation(call_sid: str):
    """Clean up conversation when call ends"""
    if call_sid in active_conversations:
        del active_conversations[call_sid]
