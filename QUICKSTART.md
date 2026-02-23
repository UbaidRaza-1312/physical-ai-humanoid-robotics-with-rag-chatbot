# 🚀 Quick Start - Panaversity RAG Chatbot

## 30-Second Setup

### Prerequisites Check
- [ ] Python 3.13+ installed
- [ ] Node.js 20.x installed
- [ ] `.env` file has API keys (Qdrant + Gemini)

### Step 1: Install Backend (1 minute)

```bash
cd "C:\Users\Star.com\Desktop\gemini book\backend"
pip install -r requirements.txt
```

### Step 2: Ingest Textbook (2 minutes)

```bash
python ingest.py
```

### Step 3: Start Backend (30 seconds)

```bash
python main.py
```

Leave this terminal open!

### Step 4: Start Frontend (1 minute)

Open **new terminal**:

```bash
cd "C:\Users\Star.com\Desktop\gemini book"
npm start
```

### Step 5: Test (30 seconds)

1. Open http://localhost:3000
2. Look for **blue chat bubble** (bottom-right)
3. Click and ask: "What is humanoid robotics?"
4. Get instant answer!

---

## 🎯 Quick Test Commands

### Check Backend Health
```bash
curl http://localhost:8000/health
```

### Test Chat API
```bash
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"query\": \"What is ROS 2?\", \"language\": \"en\"}"
```

### Re-ingest Content
```bash
python ingest.py --recreate
```

---

## 📁 All Files Created

### Backend (Python)
- ✅ `backend/main.py` - FastAPI app
- ✅ `backend/rag_engine.py` - RAG logic
- ✅ `backend/ingest.py` - Ingestion script
- ✅ `backend/requirements.txt` - Dependencies
- ✅ `backend/README.md` - Backend docs

### Frontend (React/TypeScript)
- ✅ `src/components/ChatWidget/ChatWidget.tsx` - Chat component
- ✅ `src/components/ChatWidget/ChatWidget.css` - Chat styles
- ✅ `src/components/ChatWidget/index.ts` - Exports
- ✅ `src/theme/Root.tsx` - Global wrapper
- ✅ `src/pages/client.ts` - Client-side injection

### Config
- ✅ `docusaurus.config.ts` - Updated with backend_url
- ✅ `src/css/custom.css` - Updated with chat CSS vars

### Scripts & Docs
- ✅ `start-chatbot.bat` - Windows quick start
- ✅ `start-chatbot.sh` - Linux/Mac quick start
- ✅ `IMPLEMENTATION_GUIDE.md` - Complete guide
- ✅ `backend/README.md` - Backend documentation

---

## 🎬 Demo in 3 Steps

1. **Open chat** → Ask "What is humanoid robotics?"
2. **Select text** on any page → Ask "Explain this"
3. **Toggle Urdu** → Ask "ROS 2 کیا ہے؟"

---

## ❓ Common Issues

**Chat not appearing?**
```bash
npm run clear
npm start
```

**Backend not responding?**
```bash
# Check .env has correct keys
# Restart: python main.py
```

**Ingestion fails?**
```bash
python ingest.py --recreate
```

---

## 📞 Support

- **Full Guide**: See `IMPLEMENTATION_GUIDE.md`
- **Backend Docs**: See `backend/README.md`
- **API Docs**: http://localhost:8000/docs

---

**Built with ❤️ for Panaversity Hackathon 2025**
