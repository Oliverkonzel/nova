# Team Setup Guide - Nova Voice Agent

This guide will help your team members set up and run the Nova Voice Agent on their machines.

---

## Prerequisites

Before starting, make sure you have:
- Python 3.8+ installed
- Git installed
- A code editor (VS Code, PyCharm, etc.)

---

## Step 1: Clone the Repository

```bash
# Clone the project (replace with your actual repo URL)
git clone <your-repo-url>
cd nova-voice-agent
```

---

## Step 2: Set Up Python Environment

### Option A: Using venv (Recommended)
```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Option B: Install globally (not recommended)
```bash
pip install -r requirements.txt
```

---

## Step 3: Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Open `.env` in your editor and fill in the API keys:

### Getting API Keys:

**Twilio (for phone calls):**
1. Sign up at https://console.twilio.com/
2. Get your Account SID and Auth Token from the console
3. Buy a phone number or use the provided one
4. Add these to `.env`

**OpenAI (for AI conversations):**
1. Sign up at https://platform.openai.com/
2. Go to API Keys: https://platform.openai.com/api-keys
3. Create a new API key
4. Add to `.env`

**Cal.com (for appointment booking):**
1. Sign up at https://app.cal.com/
2. Go to Settings → Developer → API Keys
3. Create a new API key
4. Add to `.env`
5. Create an event type (e.g., "free-consultation") and note the slug

**Notion (for CRM/lead logging):**
1. Sign up at https://notion.so/
2. Go to https://www.notion.so/my-integrations
3. Create a new integration and get the token
4. Create a database and share it with your integration
5. Get the database ID from the URL
6. Add both to `.env`

---

## Step 4: Test the Setup

```bash
# Start the server
cd backend
python main.py
```

You should see:
```
============================================================
Nova Voice Agent Starting...
============================================================
Twilio webhook: /webhooks/voice/incoming
Health check: /health
============================================================
```

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

Should return:
```json
{"status":"healthy","service":"Nova Voice Agent","message":"🚀 Server is running!"}
```

---

## Step 5: Set Up ngrok (for testing with phone calls)

1. Download ngrok from https://ngrok.com/download
2. Sign up and get your auth token
3. Configure ngrok:
```bash
ngrok authtoken YOUR_AUTH_TOKEN
```

4. Start ngrok in a new terminal:
```bash
ngrok http 8000
```

5. Copy the HTTPS URL (e.g., `https://abc123.ngrok-free.app`)

---

## Step 6: Configure Twilio Webhooks

1. Go to https://console.twilio.com/
2. Navigate to Phone Numbers → Manage → Active Numbers
3. Click on your phone number
4. Under "Voice Configuration":
   - A CALL COMES IN: `https://your-ngrok-url/webhooks/voice/incoming` (POST)
   - CALL STATUS CHANGES: `https://your-ngrok-url/webhooks/voice/status` (POST)
5. Click Save

---

## Step 7: Test the Complete Flow

Run the integration tests:
```bash
cd nova-voice-agent
python test_integrations.py
```

You should see:
```
✅ Cal.com:  WORKING
✅ Notion:   WORKING
🎉 All integrations are working correctly!
```

Then call your Twilio number to test the voice agent!

---

## Common Issues

### "ModuleNotFoundError"
**Solution:** Make sure you activated your virtual environment and ran `pip install -r requirements.txt`

### "Port 8000 already in use"
**Solution:**
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### "OpenAI API Error"
**Solution:**
- Check your API key is correct in `.env`
- Make sure you have credits in your OpenAI account
- Verify the key starts with `sk-proj-` or `sk-`

### "Cal.com 400 Error"
**Solution:**
- Verify your Cal.com API key starts with `cal_live_`
- Make sure you created an event type and the slug matches
- Check that the API key has proper permissions

### "Notion 400 Error"
**Solution:**
- Verify the integration has access to your database
- Check the database ID is correct
- Make sure all required properties exist in your database

---

## Team Development Workflow

### Running the Server
```bash
# Terminal 1: Start the backend
cd backend
python main.py

# Terminal 2: Start ngrok (if testing with calls)
ngrok http 8000
```

### Making Changes
1. Create a new branch for your feature
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes and test them

3. Commit and push:
```bash
git add .
git commit -m "Description of your changes"
git push origin feature/your-feature-name
```

4. Create a Pull Request for review

### Important Notes for Team Members

1. **Never commit the `.env` file** - It contains sensitive API keys
2. **Always pull latest changes** before starting work: `git pull origin main`
3. **Use virtual environments** to avoid dependency conflicts
4. **Test your changes** before committing
5. **Document any new features** you add

---

## Project Structure

```
nova-voice-agent/
├── .env                    # Your API keys (DO NOT COMMIT!)
├── .env.example           # Template for API keys (COMMIT THIS)
├── requirements.txt       # Python dependencies
├── README.md             # Main documentation
├── SETUP_FOR_TEAM.md     # This file
├── test_integrations.py  # Integration tests
│
└── backend/
    ├── main.py           # Main server file
    ├── config.py         # Configuration
    ├── models.py         # Data structures
    │
    ├── routes/
    │   ├── health.py     # Health check endpoint
    │   └── webhooks.py   # Twilio webhooks
    │
    └── services/
        ├── conversation.py # AI conversation logic
        ├── calendar.py     # Cal.com integration
        ├── sms.py         # SMS functionality
        └── crm.py         # Notion CRM integration
```

---

## Testing

Run tests before committing:
```bash
# Test integrations
python test_integrations.py

# Test booking flow
python test_booking_flow.py

# Check server health
curl http://localhost:8000/health
```

---

## Getting Help

- Check the main README.md for detailed documentation
- Check QUICKSTART.md for a quick setup guide
- Review the code comments in each file
- Ask in your team channel

---

## Next Steps After Setup

1. Review the codebase to understand how it works
2. Test the system with a real phone call
3. Check the Notion database to see logged leads
4. Verify Cal.com appointments are being created
5. Start working on your assigned features!

---

**Happy Coding! 🚀**
