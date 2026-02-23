# Panaversity RAG Chatbot - Complete Setup Guide

AI-powered chatbot for the "Physical AI & Humanoid Robotics" textbook with Retrieval-Augmented Generation (RAG).

## 🎯 Features

- ✅ **RAG-Powered**: Answers questions based on textbook content
- ✅ **Bilingual Support**: English and Urdu language support
- ✅ **Context-Aware**: Ask questions about selected text on any page
- ✅ **Embedded Widget**: Floating chat bubble integrated into Docusaurus site
- ✅ **Source Citations**: Shows which parts of the book were used for answers
- ✅ **Conversation History**: Remembers context within a session
- ✅ **Mobile Responsive**: Works perfectly on all devices

---

## 📁 Project Structure

```
gemini-book/
├── backend/                    # FastAPI Backend
│   ├── main.py                # API endpoints (/chat, /ask-with-selection, /ingest)
│   ├── rag_engine.py          # RAG logic (retrieval + generation)
│   ├── ingest.py              # Markdown ingestion script
│   └── requirements.txt       # Python dependencies
│
├── src/
│   ├── components/
│   │   └── ChatWidget/        # React Chat Widget
│   │       ├── ChatWidget.tsx
│   │       ├── ChatWidget.css
│   │       └── index.ts
│   ├── theme/
│   │   └── Root.tsx           # Global wrapper for chat widget
│   └── css/
│       └── custom.css         # Global styles (includes chat CSS vars)
│
├── docs/                      # Textbook markdown files (auto-indexed)
└── docusaurus.config.ts       # Updated with backend_url
```

---

## 🚀 Quick Start Guide

### Step 1: Install Backend Dependencies

```bash
# Navigate to project root
cd "C:\Users\Star.com\Desktop\gemini book"

# Create virtual environment (if not exists)
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### Step 2: Verify Environment Variables

Your `.env` file should have:

```env
QDRANT_URL="https://your-qdrant-cluster.qdrant.io"
QDRANT_API_KEY="your-qdrant-api-key"
GEMINI_API_KEY="your-gemini-api-key"
```

✅ **Already configured!** Your Qdrant and Gemini keys are set.

### Step 3: Ingest Textbook Content

```bash
# From the backend folder
python ingest.py

# Or to recreate the collection from scratch:
python ingest.py --recreate
```

**Expected Output:**
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

### Step 4: Start the FastAPI Backend

```bash
# From the backend folder
python main.py
```

**Expected Output:**
```
╔══════════════════════════════════════════════════════════╗
║     PANAVERSITY RAG CHATBOT API SERVER                   ║
║     Physical AI & Humanoid Robotics Textbook             ║
╚══════════════════════════════════════════════════════════╝

Starting server at http://localhost:8000

API Documentation: http://localhost:8000/docs
Health Check: http://localhost:8000/health
```

✅ **Backend is running!** Visit http://localhost:8000/docs to see the interactive API docs.

### Step 5: Install Frontend Dependencies

```bash
# From project root (in a new terminal)
cd "C:\Users\Star.com\Desktop\gemini book"
npm install
```

### Step 6: Start Docusaurus Development Server

```bash
npm start
```

The site will open at http://localhost:3000

✅ **Chat widget should appear!** Look for the blue chat bubble in the bottom-right corner.

---

## 🔧 API Endpoints

### `POST /chat`
Normal chat with textbook context.

**Request:**
```json
{
  "query": "What is ROS 2?",
  "session_id": "user123",
  "language": "en"
}
```

**Response:**
```json
{
  "response": "ROS 2 (Robot Operating System 2) is a flexible framework...",
  "sources": [
    {
      "file": "module1-ros2/intro.md",
      "module": "module1-ros2",
      "score": 0.85
    }
  ],
  "duration_ms": 234.5,
  "language": "en"
}
```

### `POST /ask-with-selection`
Ask questions about selected text on the page.

**Request:**
```json
{
  "query": "Explain this concept in simpler terms",
  "selected_text": "The transformation matrix represents the homogeneous...",
  "session_id": "user123",
  "language": "ur"
}
```

### `POST /ingest`
Re-index the textbook (admin endpoint).

**Request:**
```json
{
  "recreate": false,
  "docs_path": "/custom/path/to/docs"
}
```

### `GET /health`
Check service health.

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

## 🎨 Chat Widget Usage

### Basic Usage
1. Click the blue chat bubble in the bottom-right corner
2. Type your question in English or Urdu
3. Get answers with source citations

### Context-Aware Questions
1. **Select any text** on a textbook page
2. A red notification badge appears on the chat bubble
3. Click the chat bubble
4. Your selected text appears in a banner at the top
5. Ask questions like:
   - "Explain this"
   - "Give me an example"
   - "What does this mean?"
   - "اس کا کیا مطلب ہے؟" (Urdu)

### Language Toggle
- Click the **اردو/EN** button in the chat header
- Switches between English and Urdu responses

### Quick Start Questions
Click any of the suggested questions:
- 🤖 Humanoid Robotics
- ⚙️ ROS 2
- 🔮 Digital Twin

---

## 🎬 Demo Video Guide (< 90 seconds)

### Option 1: Screen Recording (Recommended)

**Tools:** OBS Studio (free), Loom, or built-in screen recorder

**Script:**

```
[0:00-0:05]  Show textbook homepage with chat bubble
"Introducing the AI chatbot for Physical AI & Humanoid Robotics"

[0:05-0:15]  Click chat bubble, ask: "What is humanoid robotics?"
"Ask any question about the textbook content"

[0:15-0:25]  Show answer with sources
"Get instant answers with citations to specific chapters"

[0:25-0:35]  Navigate to a page, select technical paragraph
"Select any text on the page"

[0:35-0:45]  Click chat (show selection indicator), ask: "Explain this simply"
"Ask context-aware questions about selected text"

[0:45-0:55]  Show Urdu response
"Switch to Urdu with one click - full bilingual support"

[0:55-1:05]  Show quick questions, mobile view
"Works on all devices, with quick-start suggestions"

[1:05-1:15]  Show conversation flow
"Multi-turn conversations with context memory"

[1:15-1:30]  Show API docs, Qdrant dashboard
"Powered by RAG: Qdrant vector database + Gemini AI"
```

### Option 2: NotebookLM Audio Overview

1. Go to https://notebooklm.google.com
2. Create new notebook
3. Upload your textbook markdown files
4. Generate "Audio Overview"
5. Download and use as narration over screen recording

### Option 3: Simple GIF Demo

**Tools:** ScreenToGif (free) or LICEcap

Record 3 short GIFs:
1. Chat bubble → Question → Answer
2. Text selection → Context question
3. Language toggle → Urdu response

Combine into a single demo reel.

---

## 🛠️ Troubleshooting

### Chat widget not appearing?

1. Check browser console for errors
2. Verify `Root.tsx` is in `src/theme/`
3. Clear Docusaurus cache: `npm run clear`
4. Restart dev server

### Backend not responding?

1. Check if server is running: http://localhost:8000/health
2. Verify `.env` file has correct keys
3. Check CORS settings in `main.py`
4. Ensure port 8000 is not blocked

### Ingestion fails?

1. Verify docs folder exists: `ls docs/`
2. Check Qdrant credentials in `.env`
3. Ensure collection name is unique
4. Try with `--recreate` flag

### Urdu not displaying correctly?

1. Ensure system has Urdu fonts installed
2. Check browser supports RTL text
3. Verify `chat-font-family-urdu` CSS variable
4. Test with Google Noto Nastaliq Urdu font

---

## 📦 Dependencies

### Backend
- **FastAPI** 0.115.0 - Web framework
- **Qdrant Client** 1.12.0 - Vector database
- **LangChain** 0.3.4 - RAG orchestration
- **Sentence Transformers** 3.2.1 - Multilingual embeddings
- **Google Generative AI** - Gemini LLM

### Frontend
- **React** 19.0.0 - UI framework
- **Docusaurus** 3.9.2 - Static site generator
- **TypeScript** 5.6.2 - Type safety

---

## 🔐 Security Notes

- API keys stored in `.env` (not committed to Git)
- CORS configured for localhost + GitHub Pages
- Session IDs are random and per-user
- No personal data stored

---

## 📚 Additional Resources

- **Qdrant Docs**: https://qdrant.tech/documentation/
- **LangChain Docs**: https://python.langchain.com/
- **Gemini API**: https://ai.google.dev/docs
- **Docusaurus Themes**: https://docusaurus.io/docs/api/themes

---

## 🎓 Hackathon Submission Checklist

- [x] RAG chatbot embedded in Docusaurus site
- [x] Qdrant Cloud vector database
- [x] FastAPI backend
- [x] Text selection + context-aware questions
- [x] Bilingual (English/Urdu) support
- [x] Source citations for answers
- [ ] Demo video (< 90 seconds)
- [ ] Live deployment on GitHub Pages

---

## 👨‍💻 Author

**Ubaid Raza**  
Physical AI & Humanoid Robotics Textbook  
Panaversity Hackathon 2025

---

**Built with ❤️ for the future of Physical AI**
