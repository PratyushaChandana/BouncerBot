# 🛡️ Bouncer Bot  
### AI‑Powered Content Moderation System using Apify + AWS Bedrock + Box

Bouncer Bot is an enterprise‑grade **AI content moderation system** designed for real‑world safety, automation, and compliance.  
It acts like a **digital nightclub bouncer** — detecting harmful content, issuing warnings, banning repeat offenders, and storing clean content securely for auditing.

---

# 🚀 Features

### 🔍 Multi‑Layer Moderation Pipeline
1. **Apify URL Scanner** — Scrapes and analyzes URLs found in messages  
2. **AWS Bedrock Guardrails** — Enterprise‑grade safety filters  
3. **Unified Verdict Engine** — Normalizes outputs into a single moderation verdict  

### 🛑 Strike + Ban System
- 1st violation → Warning  
- 2nd violation → Stronger warning  
- 3rd violation → Permanent ban  
- Fully session‑based and deterministic  

### 📦 Box Integration (Structured Logs)
- One JSON file per browser session  
- Stores **user + AI messages**  
- Includes moderation verdicts  
- Ideal for compliance, dashboards, and audit trails  

### 🤖 AI Response Engine
- Uses **AWS Bedrock text generation**  
- Responds only when content is clean  
- Politely refuses when content violates safety rules  

### 💬 Beautiful Chat UI
- Floating bottom‑right widget  
- Smooth animations  
- Session‑based identity  
- Works seamlessly with Flask backend  

---

# 🏗️ Architecture

```
                           ┌──────────────────────────┐
                           │        User Browser       │
                           │  - Chat Widget (JS)       │
                           │  - Session ID (UUID)      │
                           └─────────────┬────────────┘
                                         │
                                         ▼
                           ┌──────────────────────────┐
                           │        Flask API          │
                           │   /message endpoint       │
                           └─────────────┬────────────┘
                                         │
                                         ▼
                     ┌────────────────────────────────────────┐
                     │        Moderation Pipeline              │
                     │-----------------------------------------│
                     │ 1. Apify URL Scanner                    │
                     │ 2. AWS Bedrock Guardrails               │
                     │ 3. Unified Verdict Engine               │
                     └─────────────┬──────────────────────────┘
                                   │
                     Clean Content │  Violating Content
                                   │
                                   ▼
                     ┌──────────────────────────┐
                     │     AWS Bedrock LLM       │
                     │  (AI Response Generator)  │
                     └─────────────┬────────────┘
                                   │
                                   ▼
                     ┌──────────────────────────┐
                     │     Flask API returns     │
                     │     AI or Warning/Ban     │
                     └─────────────┬────────────┘
                                   │
                                   ▼
                     ┌──────────────────────────┐
                     │         Box Logs          │
                     │  - One file per session   │
                     │  - User + AI messages     │
                     │  - Verdict metadata       │
                     └──────────────────────────┘
```

---

# ⚙️ How to Run

Running Bouncer Bot locally is simple — just set your API keys and start the Flask server.

### 1️⃣ Create a `.env` file

```
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-west-2

APIFY_API_TOKEN=your_apify_token

BOX_DEVELOPER_TOKEN=your_box_token
BOX_FOLDER_ID=0
```

### 2️⃣ Install dependencies

```
pip install -r requirements.txt
```

### 3️⃣ Start the Flask app

```
python app.py
```

Your chat widget will now connect to:

```
http://localhost:5000/message
```

Open `index.html` in a browser and start chatting.

---

# 📦 Box Log Format

Each session creates:

```
session_<uuid>.json
```

Example:

```json
{
  "session_id": "uuid",
  "created_at": "...",
  "messages": [
    {
      "timestamp": "...",
      "role": "user",
      "text": "Hello",
      "verdict": "allowed"
    },
    {
      "timestamp": "...",
      "role": "assistant",
      "text": "Hi! How can I help?"
    }
  ]
}
```

---

# 🧭 Roadmap

- Dashboard for reviewing logs  
- Session replay  
- Per‑user folders in Box  
- Analytics + heatmaps  
- Multi‑tenant moderation profiles  

---

# 🏁 Summary

Bouncer Bot is a polished, production‑ready moderation system built for real‑world safety and enterprise auditing.  
It combines multi‑layer filtering, structured logging, and a clean UI to deliver a complete moderation solution.
