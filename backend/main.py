"""
FastAPI Backend for Panaversity RAG Chatbot
Provides REST API endpoints for chat, ingestion, and text-selection queries.
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass
import uvicorn

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Import RAG components
from rag_engine import RAGEngine
from ingest import MarkdownIngester

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# ============================================================================
# FastAPI App Initialization
# ============================================================================

app = FastAPI(
    title="Panaversity RAG Chatbot API",
    description="Retrieval-Augmented Generation API for Physical AI & Humanoid Robotics Textbook",
    version="1.0.0",
)

# CORS middleware - allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8080",
        "https://star-com.github.io",
        "*",  # Allow all origins for development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG engine
rag_engine = RAGEngine()

# ============================================================================
# Pydantic Models for Request/Response
# ============================================================================


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str = Field(..., description="User's question or message")
    session_id: str = Field(default="default", description="Session identifier for conversation history")
    language: str = Field(default="en", description="Response language: 'en' or 'ur'")


class ChatRequestWithSelection(BaseModel):
    """Request model for chat with selected text."""
    query: str = Field(..., description="User's question about selected text")
    selected_text: str = Field(..., description="Text selected by user on the page")
    session_id: str = Field(default="default", description="Session identifier")
    language: str = Field(default="en", description="Response language: 'en' or 'ur'")
    page_url: Optional[str] = Field(default=None, description="Current page URL for context")


class ChatResponse(BaseModel):
    """Response model for chat endpoints."""
    response: str = Field(..., description="AI-generated response")
    sources: List[dict] = Field(default_factory=list, description="Source documents used")
    duration_ms: float = Field(..., description="Response time in milliseconds")
    language: str = Field(..., description="Response language")
    has_selection: bool = Field(default=False, description="Whether selected text was provided")


class IngestRequest(BaseModel):
    """Request model for ingestion endpoint."""
    recreate: bool = Field(default=False, description="Whether to recreate the collection")
    docs_path: Optional[str] = Field(default=None, description="Custom path to docs folder")


class IngestResponse(BaseModel):
    """Response model for ingestion endpoint."""
    status: str = Field(..., description="Ingestion status")
    documents_processed: int = Field(..., description="Number of documents processed")
    chunks_created: int = Field(..., description="Number of chunks created")
    duration_seconds: float = Field(..., description="Total ingestion time")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    status: str
    qdrant: str
    gemini: str
    collection: str


# ============================================================================
# API Endpoints
# ============================================================================


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Panaversity RAG Chatbot API",
        "version": "1.0.0",
        "description": "AI chatbot for Physical AI & Humanoid Robotics textbook",
        "endpoints": {
            "chat": "POST /chat",
            "chat_with_selection": "POST /ask-with-selection",
            "ingest": "POST /ingest",
            "health": "GET /health",
        },
    }


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify all services are running.
    
    Returns:
        Health status of Qdrant and Gemini services
    """
    health = rag_engine.health_check()
    return HealthResponse(**health)


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    Main chat endpoint for asking questions about the textbook.
    
    This endpoint uses RAG (Retrieval-Augmented Generation) to:
    1. Search the textbook for relevant content
    2. Generate an answer using Gemini LLM
    3. Return the answer with source citations
    
    Args:
        request: ChatRequest with query, session_id, and language
        
    Returns:
        ChatResponse with AI answer and sources
    """
    try:
        result = rag_engine.chat(
            query=request.query,
            session_id=request.session_id,
            language=request.language,
        )
        
        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            duration_ms=result["duration_ms"],
            language=result["language"],
            has_selection=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")


@app.post("/ask-with-selection", response_model=ChatResponse, tags=["Chat"])
async def ask_with_selection(request: ChatRequestWithSelection):
    """
    Chat endpoint for questions about selected text on the page.
    
    When a user selects text on a page and asks a question about it,
    this endpoint uses both the selected text and textbook context
    to generate a relevant answer.
    
    Use cases:
    - "Explain this concept" (with technical paragraph selected)
    - "What does this mean?" (with complex sentence selected)
    - "Give me an example" (with theory selected)
    - "Translate this to Urdu" (with English text selected)
    
    Args:
        request: ChatRequestWithSelection including selected_text
        
    Returns:
        ChatResponse with contextual answer
    """
    try:
        result = rag_engine.chat(
            query=request.query,
            session_id=request.session_id,
            selected_text=request.selected_text,
            language=request.language,
        )
        
        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            duration_ms=result["duration_ms"],
            language=result["language"],
            has_selection=True,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Selection chat error: {str(e)}")


@app.post("/ingest", response_model=IngestResponse, tags=["Administration"])
async def ingest_documents(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
):
    """
    Trigger document ingestion to update the knowledge base.
    
    This endpoint:
    1. Loads all markdown files from the docs folder
    2. Chunks them into smaller pieces
    3. Generates embeddings
    4. Uploads to Qdrant vector database
    
    Can be run in background for large document sets.
    
    Args:
        request: IngestRequest with recreate flag and optional docs_path
        background_tasks: FastAPI background tasks
        
    Returns:
        IngestResponse with ingestion statistics
    """
    import time
    start_time = time.time()
    
    try:
        # Determine docs path
        if request.docs_path:
            docs_path = Path(request.docs_path)
        else:
            # Default: go up one level from backend/ to project root, then into docs/
            backend_dir = Path(__file__).parent
            docs_path = backend_dir.parent / "docs"
        
        # Initialize ingester
        ingester = MarkdownIngester()
        
        # Run ingestion (can be moved to background task for large datasets)
        ingester.ingest(str(docs_path), recreate=request.recreate)
        
        duration = time.time() - start_time
        
        return IngestResponse(
            status="success",
            documents_processed=0,  # Would need to track in ingester
            chunks_created=0,
            duration_seconds=round(duration, 2),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion error: {str(e)}")


@app.post("/clear-history", tags=["Chat"])
async def clear_history(session_id: str = "default"):
    """
    Clear conversation history for a session.
    
    Args:
        session_id: Session identifier to clear
        
    Returns:
        Status message
    """
    rag_engine.clear_history(session_id)
    return {"status": "success", "message": f"History cleared for session: {session_id}"}


@app.get("/stats", tags=["Administration"])
async def get_stats():
    """
    Get statistics about the knowledge base.
    
    Returns:
        Collection statistics from Qdrant
    """
    try:
        from rag_engine import COLLECTION_NAME
        
        collection_info = rag_engine.qdrant_client.get_collection(COLLECTION_NAME)
        
        return {
            "collection_name": COLLECTION_NAME,
            "vectors_count": collection_info.vectors_count,
            "points_count": collection_info.points_count,
            "status": str(collection_info.status),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Stats error: {str(e)}")


# ============================================================================
# Main Entry Point
# ============================================================================


def main():
    """Run the FastAPI server."""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     PANAVERSITY RAG CHATBOT API SERVER                   ║
    ║     Physical AI & Humanoid Robotics Textbook             ║
    ╚══════════════════════════════════════════════════════════╝
    
    Starting server at http://localhost:8000
    
    API Documentation: http://localhost:8000/docs
    Health Check: http://localhost:8000/health
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
    )


if __name__ == "__main__":
    main()
