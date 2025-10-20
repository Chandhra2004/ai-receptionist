# 📞 Testing Calls - Complete Guide

## Current Setup: Simulated Calls

The system currently uses **simulated calls** (no real voice). Here's how to test:

---

## ✅ Method 1: Web UI Call Simulator (Recommended)

### Steps:

1. **Start the system:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   venv\Scripts\activate
   python run.py

   # Terminal 2 - Frontend  
   cd frontend
   npm start
   ```

2. **Open browser:**
   - Go to http://localhost:3000

3. **Navigate to Call Simulator:**
   - Click "Call Simulator" in the top navigation

4. **Test different scenarios:**

   **Scenario A: AI Knows the Answer**
   - Question: "What are your hours?"
   - Expected: AI responds immediately ✅
   
   **Scenario B: AI Escalates**
   - Question: "Do you offer wedding packages?"
   - Expected: AI escalates to supervisor ⚠️
   
   **Scenario C: Custom Question**
   - Type your own question
   - See how AI responds

5. **Watch the backend console:**
   ```
   📞 INCOMING CALL
   ============================================================
   Call ID: call_CUST001_1234567890
   From: Test Customer ((555) 123-4567)
   Time: 2024-10-20T16:30:00
   ============================================================

   🎤 Customer: What are your hours?
   🤖 AI Agent: We're open Monday-Saturday 9 AM - 8 PM...

   📞 CALL ENDED
   ============================================================
   ```

---

## ✅ Method 2: API Testing with curl

### Test a call via command line:

```bash
curl -X POST http://localhost:8000/api/calls/simulate \
  -H "Content-Type: application/json" \
  -d "{
    \"customer_id\": \"CUST001\",
    \"customer_phone\": \"(555) 123-4567\",
    \"customer_name\": \"John Doe\",
    \"question\": \"What are your hours?\"
  }"
```

### Response:
```json
{
  "response": "We're open Monday-Saturday 9 AM - 8 PM, and Sunday 10 AM - 6 PM.",
  "needs_help": false,
  "help_request_id": null,
  "knowledge_used": null
}
```

---

## ✅ Method 3: Python Script

Create a test script:

```python
# test_call.py
import requests
import json

def make_test_call(question):
    """Simulate a customer call."""
    url = "http://localhost:8000/api/calls/simulate"
    
    payload = {
        "customer_id": "CUST001",
        "customer_phone": "(555) 123-4567",
        "customer_name": "Test Customer",
        "question": question
    }
    
    response = requests.post(url, json=payload)
    result = response.json()
    
    print(f"\n📞 Question: {question}")
    print(f"🤖 AI Response: {result['response']}")
    print(f"⚠️  Escalated: {result['needs_help']}")
    
    if result['help_request_id']:
        print(f"🆔 Help Request ID: {result['help_request_id']}")
    
    return result

# Test different questions
if __name__ == "__main__":
    # Known question
    make_test_call("What are your hours?")
    
    # Unknown question (will escalate)
    make_test_call("Do you offer wedding packages?")
    
    # Another known question
    make_test_call("How much is a haircut?")
```

Run it:
```bash
cd backend
python test_call.py
```

---

## ✅ Method 4: Postman Collection

Import this into Postman:

```json
{
  "info": {
    "name": "Frontdesk AI - Call Testing",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Simulate Call - Known Question",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"customer_id\": \"CUST001\",\n  \"customer_phone\": \"(555) 123-4567\",\n  \"customer_name\": \"John Doe\",\n  \"question\": \"What are your hours?\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/calls/simulate",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "calls", "simulate"]
        }
      }
    },
    {
      "name": "Simulate Call - Unknown Question",
      "request": {
        "method": "POST",
        "header": [{"key": "Content-Type", "value": "application/json"}],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"customer_id\": \"CUST002\",\n  \"customer_phone\": \"(555) 987-6543\",\n  \"customer_name\": \"Jane Smith\",\n  \"question\": \"Do you offer wedding packages?\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/calls/simulate",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "calls", "simulate"]
        }
      }
    }
  ]
}
```

---

## 🎤 Upgrading to Real Voice Calls

### You Already Have LiveKit Credentials!

I noticed in your `.env.example`:
```env
LIVEKIT_URL=wss://frontdesk-ai-4swf49dx.livekit.cloud
LIVEKIT_API_KEY=APIVcgjmx4d6J2i
LIVEKIT_API_SECRET=jOvXuh6NU8G0WrOPQt3OhlB3xiHk8dAfRZLoQUeg7QG
```

### To Enable Real Voice:

1. **Install additional dependencies:**
   ```bash
   pip install livekit livekit-api livekit-agents
   pip install deepgram-sdk  # For speech-to-text
   pip install elevenlabs     # For text-to-speech
   ```

2. **Choose speech services:**
   - **Speech-to-Text:** Deepgram, Google STT, AWS Transcribe
   - **Text-to-Speech:** ElevenLabs, Google TTS, OpenAI TTS

3. **Use the real LiveKit handler:**
   - I created `backend/livekit_real.py` for you
   - Implement the TODO sections with your chosen services
   - Replace the import in `main.py`

4. **Test with LiveKit web client:**
   - Build a simple web page with LiveKit client
   - Or use LiveKit's example apps

### Quick Real Voice Test:

```python
# In backend/
from livekit_real import livekit_real_handler

# Create a call room
call_data = await livekit_real_handler.handle_incoming_call(
    customer_id="CUST001",
    customer_phone="(555) 123-4567",
    customer_name="John Doe"
)

print(f"Room created: {call_data['room_name']}")
print(f"Customer token: {call_data['customer_token']}")

# Customer would join with this token via web/mobile app
```

---

## 🧪 Complete Test Flow

### 1. Test AI Handles Known Question

```bash
# Via UI
http://localhost:3000/simulator
Question: "What are your hours?"
Result: ✅ AI responds immediately

# Via API
curl -X POST http://localhost:8000/api/calls/simulate \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"CUST001","customer_phone":"(555)123-4567","question":"What are your hours?"}'
```

### 2. Test AI Escalation

```bash
# Via UI
Question: "Do you offer wedding packages?"
Result: ⚠️ Creates help request

# Check pending requests
http://localhost:3000/pending
```

### 3. Test Supervisor Response

```bash
# Via UI
1. Go to http://localhost:3000/pending
2. Click "Respond"
3. Type: "Yes! We offer wedding packages starting at $500..."
4. Click "Send Response"

# Via API
curl -X POST http://localhost:8000/api/requests/respond \
  -H "Content-Type: application/json" \
  -d '{
    "request_id": "YOUR_REQUEST_ID",
    "supervisor_answer": "Yes! We offer wedding packages...",
    "supervisor_id": "supervisor_1"
  }'
```

### 4. Test AI Learned

```bash
# Ask same question again
Question: "Do you offer wedding packages?"
Result: 🎉 AI now knows the answer!
```

---

## 📊 What You'll See

### Backend Console:
```
📞 INCOMING CALL
============================================================
Call ID: call_CUST001_1698765432.123
From: John Doe ((555) 123-4567)
Time: 2024-10-20T16:30:00
============================================================

🎤 Customer: What are your hours?
🤖 AI Agent: We're open Monday-Saturday 9 AM - 8 PM, and Sunday 10 AM - 6 PM.

📞 CALL ENDED
============================================================
Call ID: call_CUST001_1698765432.123
Duration: 2 exchanges
============================================================
```

### Frontend UI:
- Call result displayed
- Green checkmark if handled
- Yellow warning if escalated
- Help request ID if created

---

## 🎯 Quick Start Testing

**Fastest way to test right now:**

1. Open two terminals
2. Terminal 1: `cd backend && python run.py`
3. Terminal 2: `cd frontend && npm start`
4. Browser: http://localhost:3000/simulator
5. Click "Quick Fill" → "Simulate Call"
6. Done! 🎉

**No phone needed** - it's all simulated but shows the complete flow!

---

## 🚀 Next Steps

- ✅ Test with simulated calls (current setup)
- 🎤 Integrate real voice (LiveKit + speech services)
- 📱 Build mobile app for customers
- ☎️ Connect to phone system (Twilio)
- 💬 Add SMS notifications

For now, **use the Call Simulator** - it's the easiest way to test the complete system!
