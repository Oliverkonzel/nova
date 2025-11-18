# ⚡ QUICK START - Get Nova Running in 15 Minutes

## ✅ Step 1: Install Python Packages (2 min)

```bash
cd nova-voice-agent
pip install -r requirements.txt
```

Wait for installation to complete.

---

## ✅ Step 2: Start the Server (1 min)

```bash
cd backend
python main.py
```

You should see:
```
🚀 Nova Voice Agent Starting...
📞 Twilio webhook: /webhooks/voice/incoming
```

**✅ Open browser: http://localhost:8000/health**

Should show: `"status": "healthy"`

**Keep this terminal open!**

---

## ✅ Step 3: Install ngrok (5 min - one time only)

1. Go to: https://ngrok.com/download
2. Download for your OS
3. Extract the file
4. Sign up: https://dashboard.ngrok.com/signup
5. Get auth token: https://dashboard.ngrok.com/get-started/your-authtoken
6. Run: `ngrok authtoken YOUR_TOKEN`

---

## ✅ Step 4: Start ngrok (1 min)

**Open a NEW terminal** (keep server running in first one!)

```bash
ngrok http 8000
```

You'll see something like:
```
Forwarding   https://abc123.ngrok-free.app -> http://localhost:8000
```

**✅ Copy that HTTPS URL!** (e.g., `https://abc123.ngrok-free.app`)

**Keep this terminal open too!**

---

## ✅ Step 5: Configure Twilio (3 min)

1. Go to: https://console.twilio.com/
2. Click: **Phone Numbers** → **Manage** → **Active Numbers**
3. Click: `+1 (814) 568-5796`
4. Scroll to: **Voice Configuration**
5. Under "A CALL COMES IN":
   - Paste: `https://YOUR-NGROK-URL/webhooks/voice/incoming`
   - Select: `POST`
6. Under "CALL STATUS CHANGES":
   - Paste: `https://YOUR-NGROK-URL/webhooks/voice/status`
   - Select: `POST`
7. Click: **Save**

**Example webhook:**
```
https://abc123.ngrok-free.app/webhooks/voice/incoming
```

---

## ✅ Step 6: TEST IT! (2 min)

**Call: +1 (814) 568-5796**

### Expected Conversation:

```
Nova: "Hi! This is Nova from Orbyn dot A I. How can I help?"
You: "Hi, I need help with AI automation"
Nova: "Great! Can I get your full name?"
You: "Test User"
Nova: "Thanks! What's your phone number?"
You: "555-1234"
Nova: "Would you like to schedule a consultation?"
You: "Yes"
Nova: "I have openings Friday at 10 AM, 2 PM..."
You: "Friday at 10"
Nova: "Perfect! Booked for Friday at 10 AM. Check your phone!"
```

### What Should Happen:
- ✅ You receive an SMS
- ✅ Appointment appears in Cal.com
- ✅ Lead logged in Notion
- ✅ Server terminal shows the conversation

---

## 📊 Watching the Magic

In your server terminal, you'll see:
```
📞 Incoming call: CA...
🗣️  User said: Hi, I need help
🤖 Nova says: Great! Can I get your name?
📊 Extracted: {'name': 'Test User', 'phone': '555-1234'}
📅 Booking: Yes
✅ SMS sent!
✅ Notion lead created!
```

---

## ❌ Common Issues

### Problem: "ModuleNotFoundError"
**Fix:** `pip install -r requirements.txt`

### Problem: "Port 8000 already in use"
**Fix:** 
```bash
lsof -ti:8000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :8000   # Windows - then kill that PID
```

### Problem: "Nova doesn't respond"
**Fix:** 
- Check .env file has OpenAI key
- Check OpenAI account has credits
- Look at terminal for errors

### Problem: "No SMS received"
**Fix:**
- Phone number must be +1XXXXXXXXXX format
- Check Twilio console for SMS logs

### Problem: ngrok expired
**Fix:**
- Restart ngrok (free accounts expire after 2 hours)
- Update Twilio webhook with new URL

---

## 🎉 Success!

If you made it here and got the call working, you're done! 

### Next Steps:
1. Test it multiple times
2. Check Cal.com for bookings
3. Check Notion for leads
4. Read README.md to understand the code

---

## 📞 Quick Reference

**Your Number:** +1 (814) 568-5796  
**Health Check:** http://localhost:8000/health  
**ngrok Dashboard:** http://localhost:4040  
**Twilio Console:** https://console.twilio.com

**Keep Running:**
- Terminal 1: `python backend/main.py`
- Terminal 2: `ngrok http 8000`

---

**That's it! You're ready to demo! 🚀**
