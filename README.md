# 🛡️ Bouncer Bot  
### AI‑Powered Content Moderation System using Apify + AWS Bedrock + Local Rules + Box

Bouncer Bot is an enterprise‑grade **AI content moderation system** designed for real‑world safety, automation, and compliance.  
It acts like a **digital nightclub bouncer** — blocking harmful content, warning users, banning repeat offenders, and storing clean content securely for auditing.

---

# 🚀 Features

### 🔍 Multi‑Layer Moderation Pipeline
1. **Apify URL Scanner** — Scrapes and analyzes URLs found in messages  
2. **AWS Bedrock Guardrails** — Enterprise‑grade safety filters  
3. **Local Rule Engine** — Deterministic fallback  
4. *(Optional)* OpenAI Moderation — Disabled in this build  

### 🛑 Strike + Ban System
- 1st violation → Warning  
- 2nd violation → Stronger warning  
- 3rd violation → Permanent ban  

### 📦 Box Integration (Structured Logs)
- One JSON file per browser session  
- Stores **user + AI messages**  
- Only user messages include metadata  
- Perfect for auditing and dashboards  

### 🧠 Unified Verdict Engine
Every moderation layer returns a consistent verdict object.

### 💬 Beautiful Chat UI
- Collapsible bottom‑right widget  
- **Bouncer Bot** persona  
- Enter‑to‑send  
- Smooth animations  
- Session‑based logging  
- Works with Flask backend  

---

# 🏗️ Architecture

