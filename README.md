# 🤖 Nova Voice Agent for Orbyn.ai

An AI-powered voice agent that handles phone calls, books appointments, sends SMS confirmations, and logs to Notion CRM.

## 📞 Quick Test

Call: **+1 (814) 568-5796** (after setup)

## 🚀 Quick Start (15 minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
cd backend
python main.py
```

### 3. Expose with ngrok
```bash
# In a new terminal
ngrok http 8000
# Copy the https URL
```

### 4. Configure Twilio
1. Go to https://console.twilio.com/
2. Phone Numbers → Active Numbers → +1 (814) 568-5796
3. Voice Configuration:
   - Webhook: `https://YOUR-NGROK-URL/webhooks/voice/incoming`
   - Method: POST
4. Save

### 5. Test It!
Call: +1 (814) 568-5796

## 📁 Project Structure

```
nova-voice-agent/
├── .env                    # Your API keys (already configured!)
├── requirements.txt        # Python dependencies
├── README.md              # This file
│
└── backend/
    ├── main.py            # Start server here
    ├── config.py          # Configuration
    ├── models.py          # Data structures
    │
    ├── routes/
    │   ├── health.py      # Health check
    │   └── webhooks.py    # Twilio webhooks (IMPORTANT!)
    │
    └── services/
        ├── conversation.py # OpenAI integration
        ├── calendar.py     # Cal.com integration
        ├── sms.py         # Twilio SMS
        └── crm.py         # Notion integration
```

## 🎯 What Nova Does

1. **Answers calls** via Twilio
2. **Converses naturally** using OpenAI GPT-4
3. **Collects info**: name, phone, email, service
4. **Books appointments** in Cal.com
5. **Sends SMS** confirmations
6. **Logs to Notion** CRM

## 🔑 Your API Keys (Already Configured!)

Check your `.env` file - everything is already set up:
- ✅ Twilio (phone calls)
- ✅ OpenAI (AI conversation)
- ✅ Cal.com (scheduling)
- ✅ Notion (CRM)

## 🧪 Testing

### Test Server Health
```bash
curl http://localhost:8000/health
```

### Test Complete Flow
1. Start server: `python backend/main.py`
2. Start ngrok: `ngrok http 8000`
3. Configure Twilio with ngrok URL
4. Call: +1 (814) 568-5796
5. Have a conversation with Nova
6. Book an appointment
7. Check SMS, Cal.com, and Notion

## 📊 What to Watch

When you call, watch the terminal for:
```
📞 Incoming call: CA...
🗣️  User said: Hi, I need help
🤖 Nova says: Great! Can I get your name?
📊 Extracted: {'name': 'John'}
📅 Booking: Yes
✅ SMS sent!
✅ Notion lead created!
```

## 🔧 Troubleshooting

### "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### "Address already in use"
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9
```

### Nova doesn't respond
- Check OpenAI API key in .env
- Check you have OpenAI credits
- Look at terminal for errors

### No SMS received
- Check phone number format: +1XXXXXXXXXX
- Verify Twilio number is SMS-enabled

## 🎓 For Your Presentation

### Key Points:
1. **Fully functional** - Real phone calls, not a demo
2. **Multiple integrations** - 4 APIs working together
3. **Async architecture** - Concurrent operations
4. **Natural language** - Extracts structured data from speech

### Demo Script:
1. Show code structure
2. Start server (show logs)
3. Make live call
4. Walk through: SMS → Cal.com → Notion
5. Explain architecture

## 🚀 Adding Complexity (For Professors)

Easy additions:
- **Sentiment analysis** - Detect caller frustration
- **Lead scoring** - ML model for conversion prediction
- **A/B testing** - Test different scripts
- **Analytics dashboard** - Real-time call metrics
- **Voice biometrics** - Speaker verification
- **Multi-language** - Spanish/English detection

## 📝 Important Files

Start reading here:
1. `backend/routes/webhooks.py` - Main call flow
2. `backend/services/conversation.py` - AI logic
3. `backend/services/calendar.py` - Booking logic

## 🆘 Need Help?

Common commands:
```bash
# Start server
cd backend && python main.py

# Start ngrok
ngrok http 8000

# Check dependencies
pip list

# Test health
curl http://localhost:8000/health
```

## 🎉 You're Ready!

Everything is configured and ready to go. Just:
1. Install dependencies
2. Start server
3. Start ngrok
4. Configure Twilio
5. Call and test!

Good luck with your senior design project! 🚀
