# Panaversity RAG Chatbot - Complete Implementation Guide

## 🎯 Overview

This guide provides step-by-step instructions to build and deploy a **Retrieval-Augmented Generation (RAG) chatbot** for the Physical AI & Humanoid Robotics textbook.

### Core Features
✅ RAG-powered answers from textbook content  
✅ Bilingual support (English + Urdu)  
✅ Context-aware questions from selected text  
✅ Embedded floating chat widget  
✅ Source citations for all answers  
✅ Conversation history within sessions  

### Tech Stack
- **Backend**: FastAPI (Python)
- **Vector DB**: Qdrant Cloud (Free Tier)
- **LLM**: Google Gemini 1.5 Flash (Free)
- **Embeddings**: Sentence Transformers (Multilingual)
- **Frontend**: React + Docusaurus
- **Chat UI**: Custom ChatKit-style widget

---

## 📋 Prerequisites

1. **Python 3.13+** installed
2. **Node.js 20.x** installed
3. **Qdrant Cloud** account (free tier)
4. **Google AI Studio** account (for Gemini API)
5. **Git** (for version control)

---

## 📁 Step 1: Project Structure

Your final structure should look like this:

```
gemini-book/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── rag_engine.py           # RAG logic
│   ├── ingest.py               # Ingestion script
│   ├── requirements.txt        # Python dependencies
│   └── README.md              # Backend docs
│
├── src/
│   ├── components/
│   │   └── ChatWidget/
│   │       ├── ChatWidget.tsx  # React chat component
│   │       ├── ChatWidget.css  # Chat styles
│   │       └── index.ts        # Exports
│   ├── theme/
│   │   └── Root.tsx           # Global wrapper
│   └── css/
│       └── custom.css         # Global styles
│
├── docs/                       # Textbook markdown
├── .env                        # Environment variables
├── docusaurus.config.ts        # Docusaurus config
├── start-chatbot.bat          # Windows quick start
└── start-chatbot.sh           # Linux/Mac quick start
```

---

## 🔑 Step 2: Set Up Qdrant Cloud (Free Tier)

### 2.1 Create Qdrant Account

1. Go to https://cloud.qdrant.io/
2. Click **"Sign Up"** (use GitHub or Google)
3. Verify your email

### 2.2 Create a Cluster

1. Click **"Create New Cluster"**
2. Choose **Free Tier** (1 GB storage, enough for 100k+ vectors)
3. Select region (closest to you)
4. Click **"Create"**

### 2.3 Get API Credentials

1. Click on your cluster
2. Go to **"API Keys"** tab
3. Click **"Create API Key"**
   - Name: `panaversity-chatbot`
   - Access: `Read + Write`
4. Copy the API key (save it securely)
5. Copy the **Cluster URL** (looks like: `https://xxx-xxx-xxx.us-east4-0.gcp.cloud.qdrant.io`)

### 2.4 Update .env File

```env
QDRANT_URL="https://your-cluster-id.us-east4-0.gcp.cloud.qdrant.io"
QDRANT_API_KEY="your-api-key-here"
GEMINI_API_KEY="your-gemini-api-key"
```

---

## 🔑 Step 3: Get Gemini API Key (Free)

### 3.1 Create Google AI Studio Account

1. Go to https://aistudio.google.com/
2. Sign in with Google account
3. Click **"Get API Key"**

### 3.2 Create API Key

1. Click **"Create API Key"**
2. Select your Google Cloud project (or create new)
3. Copy the API key

### 3.3 Add to .env

```env
GEMINI_API_KEY="AIzaSy..."
```

---

## 🐍 Step 4: Install Backend Dependencies

### 4.1 Navigate to Project

```bash
cd "C:\Users\Star.com\Desktop\gemini book"
```

### 4.2 Create Virtual Environment (if not exists)

```bash
# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

### 4.3 Activate Virtual Environment

```bash
# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 4.4 Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**Dependencies installed:**
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `qdrant-client` - Vector DB client
- `langchain` - RAG orchestration
- `langchain-qdrant` - Qdrant integration
- `langchain-google-genai` - Gemini integration
- `sentence-transformers` - Multilingual embeddings
- `python-dotenv` - Environment variables
- `fastapi-cors` - CORS support

---

## 📚 Step 5: Ingest Textbook Content

### 5.1 How Ingestion Works

The `ingest.py` script:
1. **Scans** all `.md` and `.mdx` files in `/docs`
2. **Chunks** content into 500-character pieces (with 150 char overlap)
3. **Generates embeddings** using multilingual Sentence Transformers
4. **Uploads** to Qdrant with metadata (source file, module, etc.)

### 5.2 Run Ingestion

```bash
# From backend folder
python ingest.py
```

### 5.3 Expected Output

```
============================================================
🎓 PANAVERSITY RAG INGESTION PIPELINE
============================================================

📦 Creating new collection: panaversity_textbook
   Vector dimension: 384
✅ Collection 'panaversity_textbook' created successfully!

📚 Loading markdown files from: ../docs
   Found 15 .md files and 3 .mdx files
   ✅ Loaded 18 documents

✂️  Chunking documents...
   Chunk size: 500 characters
   Overlap: 150 characters
   ✅ Created 142 chunks

🔢 Generating embeddings...
   Processed 142/142 chunks
   ✅ Embeddings generated successfully

⬆️  Uploading to Qdrant Cloud...
   Uploaded 142/142 chunks
   ✅ Upload complete!

✅ INGESTION COMPLETE!
   Total chunks: 142
   Duration: 8.45 seconds
```

### 5.4 Verify in Qdrant Dashboard

1. Go to Qdrant Cloud dashboard
2. Click on your cluster
3. Go to **"Collections"** tab
4. You should see `panaversity_textbook` with ~142 points

---

## 🚀 Step 6: Start FastAPI Backend

### 6.1 Run the Server

```bash
# From backend folder
python main.py
```

### 6.2 Expected Output

```
╔══════════════════════════════════════════════════════════╗
║     PANAVERSITY RAG CHATBOT API SERVER                   ║
║     Physical AI & Humanoid Robotics Textbook             ║
╚══════════════════════════════════════════════════════════╝

Starting server at http://localhost:8000

API Documentation: http://localhost:8000/docs
Health Check: http://localhost:8000/health
```

### 6.3 Test the API

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "qdrant": "connected",
  "gemini": "connected",
  "collection": "panaversity_textbook"
}
```

**Test Chat:**
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is ROS 2?", "language": "en"}'
```

### 6.4 Interactive API Docs

Open http://localhost:8000/docs to see Swagger UI with all endpoints.

---

## ⚛️ Step 7: Frontend Setup

### 7.1 Install Node Dependencies

```bash
# From project root
npm install
```

### 7.2 Verify Chat Widget Files

Ensure these files exist:
- `src/components/ChatWidget/ChatWidget.tsx`
- `src/components/ChatWidget/ChatWidget.css`
- `src/components/ChatWidget/index.ts`
- `src/theme/Root.tsx`

### 7.3 Update Docusaurus Config

Your `docusaurus.config.ts` should have:

```typescript
customFields: {
  backend_url: 'http://localhost:8000',
},

themeConfig: {
  wrapper: {
    enabled: true,
  },
  // ... rest of config
},
```

---

## 🎨 Step 8: Start Docusaurus Frontend

### 8.1 Run Development Server

```bash
npm start
```

### 8.2 Open Browser

Site opens at http://localhost:3000

### 8.3 Verify Chat Widget

Look for:
- **Blue chat bubble** in bottom-right corner
- **Red notification badge** when text is selected
- Smooth animations and modern UI

---

## 💬 Step 9: Test the Chatbot

### 9.1 Basic Chat

1. Click chat bubble
2. Type: "What is humanoid robotics?"
3. Get answer with sources

### 9.2 Context-Aware Questions

1. Navigate to any textbook page
2. **Select a paragraph** of text
3. See **red badge** on chat bubble
4. Click chat bubble
5. Selected text appears in banner
6. Ask: "Explain this in simpler terms"
7. Get contextual answer

### 9.3 Urdu Support

1. Click **اردو** button in chat header
2. Ask: "Humanoid robotics کیا ہے؟"
3. Get Urdu response

### 9.4 Quick Questions

Click suggested chips:
- 🤖 Humanoid Robotics
- ⚙️ ROS 2
- 🔮 Digital Twin

---

## 🔧 Step 10: API Endpoint Details

### POST /chat

**Purpose:** Normal chat with textbook context

**Request:**
```json
{
  "query": "What is a digital twin?",
  "session_id": "user_123",
  "language": "en"
}
```

**Response:**
```json
{
  "response": "A digital twin is a virtual representation...",
  "sources": [
    {
      "file": "module2-digital-twin/intro.mdx",
      "module": "module2-digital-twin",
      "score": 0.87
    }
  ],
  "duration_ms": 342.5,
  "language": "en"
}
```

### POST /ask-with-selection

**Purpose:** Ask about selected text

**Request:**
```json
{
  "query": "What does this equation mean?",
  "selected_text": "T = [R | t; 0 | 1]",
  "session_id": "user_123",
  "language": "ur"
}
```

**Response:**
```json
{
  "response": "یہ مساوات ایک ہوموجینیس ٹرانسفارمیشن میٹرکس...",
  "sources": [...],
  "has_selection": true
}
```

### POST /ingest

**Purpose:** Re-index textbook (admin)

**Request:**
```json
{
  "recreate": true,
  "docs_path": "/custom/path"
}
```

### GET /health

**Purpose:** Check service status

**Response:**
```json
{
  "status": "healthy",
  "qdrant": "connected",
  "gemini": "connected",
  "collection": "panaversity_textbook"
}
```

---

## 🎬 Step 11: Create Demo Video (< 90 seconds)

### Option A: Screen Recording (Recommended)

**Tools:**
- OBS Studio (free): https://obsproject.com/
- Loom (free tier): https://www.loom.com/
- Windows Game Bar: `Win + G`

**Shot List:**

| Time | Scene | Action |
|------|-------|--------|
| 0:00-0:05 | Homepage | Show textbook site with chat bubble |
| 0:05-0:15 | Chat open | Ask "What is humanoid robotics?" |
| 0:15-0:25 | Answer | Show response with source citations |
| 0:25-0:35 | Text selection | Select paragraph on a page |
| 0:35-0:45 | Context question | Ask "Explain this simply" |
| 0:45-0:55 | Urdu mode | Toggle to Urdu, ask question |
| 0:55-1:05 | Mobile view | Show responsive design |
| 1:05-1:15 | API docs | Show backend at localhost:8000/docs |
| 1:15-1:30 | Qdrant dashboard | Show vector DB in cloud |

**Voiceover Script:**

> "Introducing the AI chatbot for the Physical AI & Humanoid Robotics textbook.
> 
> Ask any question and get instant answers with citations.
> Select text on any page to ask context-aware questions.
> Switch to Urdu with one click for full bilingual support.
> 
> Powered by RAG: Qdrant vector database and Google Gemini AI.
> Built for Panaversity Hackathon 2025."

### Option B: GIF Demo

**Tools:** ScreenToGif (free)

Record 3 GIFs:
1. Chat interaction (question → answer)
2. Text selection workflow
3. Language toggle

Combine into collage.

---

## 🛠️ Step 12: Troubleshooting

### Chat Widget Not Appearing

**Check:**
1. Browser console for errors (`F12`)
2. `Root.tsx` exists in `src/theme/`
3. Clear Docusaurus cache: `npm run clear`
4. Restart: `npm start`

### Backend Not Responding

**Check:**
1. Server running: `http://localhost:8000/health`
2. `.env` file has correct keys
3. Port 8000 not blocked by firewall
4. CORS settings in `main.py`

### Ingestion Fails

**Check:**
1. Docs folder exists: `ls docs/`
2. Qdrant credentials valid
3. Collection name unique
4. Try: `python ingest.py --recreate`

### Gemini API Error

**Check:**
1. API key valid: https://aistudio.google.com/app/apikey
2. API quota not exceeded
3. Model name correct: `gemini-1.5-flash`
4. Network connectivity

### Urdu Not Displaying

**Check:**
1. System has Urdu fonts
2. Browser supports RTL
3. CSS variable: `--chat-font-family-urdu`
4. Install Google Noto Nastaliq Urdu font

---

## 📊 Step 13: Monitor Usage

### Qdrant Dashboard

1. Go to Qdrant Cloud
2. View collection stats
3. Monitor vector count
4. Check API calls

### Backend Logs

```bash
# Watch logs in real-time
tail -f backend/logs.txt
```

### Browser DevTools

1. Open `F12` DevTools
2. Go to Network tab
3. Filter by `/chat` or `/ask-with-selection`
4. Inspect requests/responses

---

## 🚀 Step 14: Deploy to Production

### 14.1 Deploy Backend

**Options:**
- **Railway**: https://railway.app/ (easiest)
- **Render**: https://render.com/
- **Hugging Face Spaces**: https://huggingface.co/spaces (free)
- **Google Cloud Run**: https://cloud.google.com/run

**Railway Deployment:**

1. Push code to GitHub
2. Go to https://railway.app/
3. Click **"New Project"** → **"Deploy from GitHub"**
4. Select your repo
5. Add environment variables:
   - `QDRANT_URL`
   - `QDRANT_API_KEY`
   - `GEMINI_API_KEY`
6. Deploy!

### 14.2 Update Frontend Config

Change `docusaurus.config.ts`:

```typescript
customFields: {
  backend_url: 'https://your-backend.railway.app',
},
```

### 14.3 Deploy to GitHub Pages

```bash
npm run build
npm run deploy
```

Your site deploys to: `https://your-username.github.io/your-repo/`

---

## ✅ Hackathon Submission Checklist

- [ ] RAG chatbot embedded in Docusaurus
- [ ] Qdrant Cloud vector database configured
- [ ] FastAPI backend running
- [ ] Text selection + context questions working
- [ ] Bilingual (English/Urdu) support
- [ ] Source citations showing
- [ ] Demo video recorded (< 90 sec)
- [ ] Live deployment on GitHub Pages
- [ ] Code pushed to GitHub (public repo)
- [ ] README with setup instructions

---

## 📚 Resources

### Official Documentation

- **Qdrant**: https://qdrant.tech/documentation/
- **LangChain**: https://python.langchain.com/docs/get_started/introduction
- **Gemini API**: https://ai.google.dev/docs
- **FastAPI**: https://fastapi.tiangolo.com/
- **Docusaurus**: https://docusaurus.io/docs

### Tutorials

- RAG with Qdrant: https://qdrant.tech/documentation/tutorials/
- LangChain + Qdrant: https://python.langchain.com/docs/integrations/vectorstores/qdrant
- Docusaurus Theming: https://docusaurus.io/docs/swizzling

### Communities

- Qdrant Discord: https://discord.gg/qdrant
- LangChain Discord: https://discord.gg/langchain
- Docusaurus Discord: https://discord.gg/docusaurus

---

## 👨‍💻 About This Project

**Built by:** Ubaid Raza  
**Hackathon:** Panaversity 2025  
**Project:** Physical AI & Humanoid Robotics Textbook  
**Tech Stack:** FastAPI + Qdrant + Gemini + Docusaurus  

---

**🎓 Good luck with your hackathon submission!**
