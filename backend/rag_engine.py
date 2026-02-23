"""
RAG Engine for Panaversity Chatbot
Handles retrieval from Qdrant and generation with Gemini LLM.
Supports bilingual (Urdu/English) queries and responses.
"""

import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime

from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer
from google import genai
from google.genai import types

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
COLLECTION_NAME = "book"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"

# RAG configuration
TOP_K_RESULTS = 5  # Number of chunks to retrieve
SCORE_THRESHOLD = 0.3  # Minimum similarity score


@dataclass
class RetrievedChunk:
    """Represents a retrieved chunk from the vector database."""
    text: str
    source_file: str
    module: str
    score: float
    chunk_id: int


@dataclass
class ChatMessage:
    """Represents a chat message."""
    role: str  # 'user' or 'assistant'
    content: str
    timestamp: str


class RAGEngine:
    """
    Retrieval-Augmented Generation engine for the Panaversity chatbot.
    Combines Qdrant vector search with Gemini LLM for contextual answers.
    """
    
    def __init__(self):
        """Initialize the RAG engine with Qdrant client and Gemini model."""
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )

        # Initialize embedding model
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

        # Initialize Gemini (new SDK)
        if GEMINI_API_KEY:
            self.gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        else:
            self.gemini_client = None
            print("⚠️  Warning: GEMINI_API_KEY not set. LLM features will be limited.")

        # Conversation history (per session)
        self.conversation_history: Dict[str, List[ChatMessage]] = {}
    
    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a query string.
        
        Args:
            query: The query text
            
        Returns:
            Embedding vector as list of floats
        """
        embedding = self.embedding_model.encode(
            query,
            convert_to_numpy=True,
            show_progress_bar=False,
        )
        return embedding.tolist()
    
    def retrieve_chunks(
        self,
        query: str,
        top_k: int = TOP_K_RESULTS,
        score_threshold: float = SCORE_THRESHOLD,
        filter_module: Optional[str] = None,
    ) -> List[RetrievedChunk]:
        """
        Retrieve relevant chunks from Qdrant based on query.
        
        Args:
            query: User query
            top_k: Number of results to return
            score_threshold: Minimum similarity score
            filter_module: Optional module filter
            
        Returns:
            List of retrieved chunks
        """
        # Generate query embedding
        query_embedding = self.embed_query(query)

        # Build filter if module is specified
        query_filter = None
        if filter_module:
            query_filter = models.Filter(
                must=[
                    models.FieldCondition(
                        key="module",
                        match=models.MatchValue(value=filter_module),
                    )
                ]
            )

        # Search Qdrant (new API)
        search_results = self.qdrant_client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,
            query_filter=query_filter,
            limit=top_k,
            score_threshold=score_threshold,
        )

        # Convert to RetrievedChunk objects
        chunks = []
        for result in search_results.points:
            chunk = RetrievedChunk(
                text=result.payload.get("text", ""),
                source_file=result.payload.get("source_file", "unknown"),
                module=result.payload.get("module", "unknown"),
                score=result.score,
                chunk_id=result.payload.get("chunk_id", 0),
            )
            chunks.append(chunk)

        return chunks
    
    def build_context(self, chunks: List[RetrievedChunk]) -> str:
        """
        Build context string from retrieved chunks.
        
        Args:
            chunks: List of retrieved chunks
            
        Returns:
            Formatted context string
        """
        if not chunks:
            return "No relevant context found in the textbook."
        
        context_parts = []
        for i, chunk in enumerate(chunks, 1):
            context_parts.append(
                f"[Source: {chunk.source_file} | Module: {chunk.module}]\n"
                f"{chunk.text}\n"
            )
        
        return "\n---\n".join(context_parts)
    
    def generate_response(
        self,
        query: str,
        context: str,
        selected_text: Optional[str] = None,
        conversation_history: Optional[List[ChatMessage]] = None,
        language: str = "en",
    ) -> str:
        """
        Generate response using Gemini LLM with RAG context.
        
        Args:
            query: User query
            context: Retrieved context from textbook
            selected_text: Optional text selected by user on the page
            conversation_history: Optional conversation history
            language: Response language ('en' or 'ur' for Urdu)
            
        Returns:
            Generated response
        """
        # Build prompt
        system_prompt = self._build_system_prompt(language)
        
        # Add selected text context if provided
        selection_context = ""
        if selected_text:
            selection_context = f"""
SELECTED TEXT FROM PAGE:
```
{selected_text}
```

The user has selected the above text on the current page and is asking a question about it. 
Use this selected text as additional context when answering.
"""
        
        # Add conversation history if provided
        history_context = ""
        if conversation_history and len(conversation_history) > 0:
            history_context = "\n\nCONVERSATION HISTORY:\n"
            for msg in conversation_history[-5:]:  # Last 5 messages
                role = "User" if msg.role == "user" else "Assistant"
                history_context += f"{role}: {msg.content}\n"
        
        # Build full prompt
        prompt = f"""{system_prompt}

{selection_context}

RELEVANT CONTEXT FROM TEXTBOOK:
```
{context}
```
{history_context}

USER QUESTION: {query}

Please provide a helpful, accurate answer based on the textbook context above."""

        # Generate response with Gemini (new SDK)
        if self.gemini_client:
            try:
                response = self.gemini_client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        temperature=0.7,
                        top_p=0.8,
                        top_k=40,
                        max_output_tokens=1024,
                    ),
                )
                return response.text
            except Exception as e:
                return f"I apologize, but I encountered an error generating a response: {str(e)}"
        else:
            # Fallback: return context directly
            return f"Based on the textbook:\n\n{context}"
    
    def _build_system_prompt(self, language: str) -> str:
        """
        Build system prompt based on language preference.
        
        Args:
            language: 'en' for English, 'ur' for Urdu
            
        Returns:
            System prompt string
        """
        if language == "ur":
            return """آپ پانورسٹی ٹیکنالوجیز کے لیے ایک مددگار AI اسسٹنٹ ہیں۔ آپ کا کام "Physical AI & Humanoid Robotics" کی کتاب سے سوالات کے جوابات دینا ہے۔

اہداف:
- کتاب کے مواد کی بنیاد پر درست اور مفید جوابات دیں
- اردو یا انگلش میں جواب دیں (جو صارف استعمال کرے)
- تکنیکی اصطلاحات کو انگلش میں رکھیں جہاں ضروری ہو
- اگر جواب کتاب میں نہ ملے تو واضح کریں

جوابات مختصر اور واضح رکھیں۔"""
        else:
            return """You are a helpful AI assistant for Panaversity Technologies. Your task is to answer questions about the "Physical AI & Humanoid Robotics" textbook.

Goals:
- Provide accurate and helpful answers based on the textbook content
- Respond in the same language the user uses (English or Urdu)
- Keep technical terms in English where appropriate
- If the answer is not in the textbook, clearly state that

Keep answers concise and clear."""
    
    def chat(
        self,
        query: str,
        session_id: str = "default",
        selected_text: Optional[str] = None,
        language: str = "en",
    ) -> Dict[str, Any]:
        """
        Main chat endpoint with RAG.
        
        Args:
            query: User query
            session_id: Session identifier for conversation history
            selected_text: Optional text selected on page
            language: Response language preference
            
        Returns:
            Dictionary with response and metadata
        """
        start_time = datetime.now()
        
        # Retrieve relevant chunks
        chunks = self.retrieve_chunks(query)
        
        # Build context
        context = self.build_context(chunks)
        
        # Get conversation history
        history = self.conversation_history.get(session_id, [])
        
        # Generate response
        response = self.generate_response(
            query=query,
            context=context,
            selected_text=selected_text,
            conversation_history=history,
            language=language,
        )
        
        # Update conversation history
        if session_id not in self.conversation_history:
            self.conversation_history[session_id] = []
        
        self.conversation_history[session_id].append(
            ChatMessage(role="user", content=query, timestamp=datetime.now().isoformat())
        )
        self.conversation_history[session_id].append(
            ChatMessage(role="assistant", content=response, timestamp=datetime.now().isoformat())
        )
        
        # Keep history limited (last 10 messages)
        if len(self.conversation_history[session_id]) > 10:
            self.conversation_history[session_id] = self.conversation_history[session_id][-10:]
        
        # Calculate duration
        duration = (datetime.now() - start_time).total_seconds()
        
        return {
            "response": response,
            "sources": [
                {
                    "file": chunk.source_file,
                    "module": chunk.module,
                    "score": round(chunk.score, 3),
                }
                for chunk in chunks
            ],
            "context_used": context,
            "duration_ms": round(duration * 1000, 2),
            "language": language,
        }
    
    def clear_history(self, session_id: str = "default"):
        """Clear conversation history for a session."""
        if session_id in self.conversation_history:
            del self.conversation_history[session_id]
    
    def health_check(self) -> Dict[str, Any]:
        """Check if all services are healthy."""
        try:
            # Check Qdrant
            collections = self.qdrant_client.get_collections()
            qdrant_healthy = COLLECTION_NAME in [c.name for c in collections.collections]
            
            # Check Gemini
            gemini_healthy = self.gemini_model is not None
            
            return {
                "status": "healthy" if qdrant_healthy and gemini_healthy else "degraded",
                "qdrant": "connected" if qdrant_healthy else "disconnected",
                "gemini": "connected" if gemini_healthy else "disconnected",
                "collection": COLLECTION_NAME,
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
            }
