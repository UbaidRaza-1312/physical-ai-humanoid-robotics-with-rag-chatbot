"""
Markdown Ingestion Script for Panaversity RAG Chatbot
Chunks all Docusaurus markdown files and uploads embeddings to Qdrant Cloud.
Supports both English and Urdu text with multilingual embeddings.
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any
import hashlib
from datetime import datetime

# LangChain imports
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
COLLECTION_NAME = "book"
EMBEDDING_MODEL = "paraphrase-multilingual-MiniLM-L12-v2"  # Supports Urdu & English

# Chunking configuration - optimized for textif catbot folder is not need so
#  content
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 150  # Overlap between chunks for context


class MarkdownIngester:
    """Handles ingestion of Docusaurus markdown files into Qdrant."""
    
    def __init__(self):
        """Initialize the ingester with Qdrant client and embedding model."""
        print(f"🚀 Initializing Panaversity RAG Ingestion System...")
        
        # Validate environment variables
        if not QDRANT_URL or not QDRANT_API_KEY:
            raise ValueError("QDRANT_URL and QDRANT_API_KEY must be set in .env file")
        
        # Initialize Qdrant client
        self.qdrant_client = QdrantClient(
            url=QDRANT_URL,
            api_key=QDRANT_API_KEY,
        )
        
        # Initialize multilingual embedding model
        print(f"📊 Loading embedding model: {EMBEDDING_MODEL}")
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
        
        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", "## ", "# ", ". ", " ", ""],
        )
        
        print("✅ Initialization complete!\n")
    
    def get_embedding_dimension(self) -> int:
        """Get the dimension of embeddings from the model."""
        test_embedding = self.embedding_model.encode("test")
        return len(test_embedding)
    
    def create_collection_if_not_exists(self):
        """Create Qdrant collection if it doesn't exist."""
        dimension = self.get_embedding_dimension()
        
        collections = self.qdrant_client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if COLLECTION_NAME not in collection_names:
            print(f"📦 Creating new collection: {COLLECTION_NAME}")
            print(f"   Vector dimension: {dimension}")
            
            self.qdrant_client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=dimension,
                    distance=models.Distance.COSINE,
                ),
                # Add metadata fields for filtering
                optimizers_config=models.OptimizersConfigDiff(
                    default_segment_number=2,
                    indexing_threshold=20000,
                ),
            )
            
            # Create payload index for faster filtering
            self.qdrant_client.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name="source_file",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )
            self.qdrant_client.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name="module",
                field_schema=models.PayloadSchemaType.KEYWORD,
            )
            
            print(f"✅ Collection '{COLLECTION_NAME}' created successfully!\n")
        else:
            print(f"✅ Collection '{COLLECTION_NAME}' already exists\n")
    
    def load_markdown_files(self, docs_path: str) -> List[Document]:
        """
        Load all markdown files from Docusaurus docs folder.
        
        Args:
            docs_path: Path to the docs directory
            
        Returns:
            List of LangChain Document objects
        """
        print(f"📚 Loading markdown files from: {docs_path}")
        
        if not os.path.exists(docs_path):
            raise FileNotFoundError(f"Docs directory not found: {docs_path}")
        
        # Count files
        md_files = list(Path(docs_path).rglob("*.md"))
        mdx_files = list(Path(docs_path).rglob("*.mdx"))
        total_files = len(md_files) + len(mdx_files)
        print(f"   Found {len(md_files)} .md files and {len(mdx_files)} .mdx files")
        
        documents = []
        
        # Load .md files
        for md_file in md_files:
            try:
                loader = TextLoader(str(md_file), encoding='utf-8')
                docs = loader.load()
                
                # Add metadata
                for doc in docs:
                    doc.metadata["source_file"] = str(md_file.relative_to(docs_path))
                    doc.metadata["file_path"] = str(md_file)
                    doc.metadata["module"] = md_file.parent.name
                    doc.metadata["file_type"] = "markdown"
                    doc.metadata["last_modified"] = datetime.fromtimestamp(
                        md_file.stat().st_mtime
                    ).isoformat()
                
                documents.extend(docs)
            except Exception as e:
                print(f"   ⚠️  Error loading {md_file.name}: {str(e)}")
        
        # Load .mdx files (treat as text for now)
        for mdx_file in mdx_files:
            try:
                loader = TextLoader(str(mdx_file), encoding='utf-8')
                docs = loader.load()
                
                # Add metadata
                for doc in docs:
                    doc.metadata["source_file"] = str(mdx_file.relative_to(docs_path))
                    doc.metadata["file_path"] = str(mdx_file)
                    doc.metadata["module"] = mdx_file.parent.name
                    doc.metadata["file_type"] = "mdx"
                    doc.metadata["last_modified"] = datetime.fromtimestamp(
                        mdx_file.stat().st_mtime
                    ).isoformat()
                
                documents.extend(docs)
            except Exception as e:
                print(f"   ⚠️  Error loading {mdx_file.name}: {str(e)}")
        
        print(f"   ✅ Loaded {len(documents)} documents\n")
        return documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for better retrieval.
        
        Args:
            documents: List of documents to chunk
            
        Returns:
            List of chunked documents
        """
        print(f"✂️  Chunking documents...")
        print(f"   Chunk size: {CHUNK_SIZE} characters")
        print(f"   Overlap: {CHUNK_OVERLAP} characters")
        
        chunks = self.text_splitter.split_documents(documents)
        
        # Add chunk IDs
        for i, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = i
            chunk.metadata["total_chunks"] = len(chunks)
        
        print(f"   ✅ Created {len(chunks)} chunks\n")
        return chunks
    
    def generate_embeddings(self, chunks: List[Document]) -> List[List[float]]:
        """
        Generate embeddings for all chunks using multilingual model.
        
        Args:
            chunks: List of document chunks
            
        Returns:
            List of embedding vectors
        """
        print(f"🔢 Generating embeddings...")
        texts = [chunk.page_content for chunk in chunks]
        
        # Generate embeddings in batches
        embeddings = []
        batch_size = 32
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_embeddings = self.embedding_model.encode(
                batch,
                show_progress_bar=False,
                convert_to_numpy=True,
            )
            embeddings.extend(batch_embeddings.tolist())
            
            if (i + batch_size) % 100 == 0 or i + batch_size >= len(texts):
                processed = min(i + batch_size, len(texts))
                print(f"   Processed {processed}/{len(texts)} chunks")
        
        print(f"   ✅ Embeddings generated successfully\n")
        return embeddings
    
    def upload_to_qdrant(self, chunks: List[Document], embeddings: List[List[float]]):
        """
        Upload chunks and embeddings to Qdrant vector database.
        
        Args:
            chunks: List of document chunks
            embeddings: List of embedding vectors
        """
        print(f"⬆️  Uploading to Qdrant Cloud...")
        print(f"   Collection: {COLLECTION_NAME}")
        print(f"   URL: {QDRANT_URL}")
        
        # Prepare points for Qdrant
        points = []
        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            # Create unique ID for each chunk
            chunk_id = hashlib.md5(
                f"{chunk.metadata['source_file']}_{i}".encode()
            ).hexdigest()
            
            points.append(
                models.PointStruct(
                    id=chunk_id,
                    vector=embedding,
                    payload={
                        "text": chunk.page_content,
                        "source_file": chunk.metadata.get("source_file", "unknown"),
                        "file_path": chunk.metadata.get("file_path", "unknown"),
                        "module": chunk.metadata.get("module", "unknown"),
                        "file_type": chunk.metadata.get("file_type", "markdown"),
                        "chunk_id": chunk.metadata.get("chunk_id", i),
                        "total_chunks": chunk.metadata.get("total_chunks", len(chunks)),
                        "ingested_at": datetime.now().isoformat(),
                    },
                )
            )
        
        # Upload in batches
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i:i + batch_size]
            self.qdrant_client.upsert(
                collection_name=COLLECTION_NAME,
                points=batch,
            )
            print(f"   Uploaded {min(i + batch_size, len(points))}/{len(points)} chunks")
        
        print(f"   ✅ Upload complete!\n")
    
    def ingest(self, docs_path: str, recreate: bool = False):
        """
        Full ingestion pipeline: load → chunk → embed → upload.
        
        Args:
            docs_path: Path to docs directory
            recreate: If True, delete and recreate collection
        """
        start_time = datetime.now()
        print("=" * 60)
        print("🎓 PANAVERSITY RAG INGESTION PIPELINE")
        print("=" * 60 + "\n")
        
        # Delete collection if recreating
        if recreate:
            print(f"🗑️  Deleting existing collection: {COLLECTION_NAME}")
            try:
                self.qdrant_client.delete_collection(COLLECTION_NAME)
                print(f"   ✅ Collection deleted\n")
            except Exception as e:
                print(f"   ⚠️  Could not delete collection: {e}\n")
        
        # Create collection
        self.create_collection_if_not_exists()
        
        # Load documents
        documents = self.load_markdown_files(docs_path)
        
        if not documents:
            print("❌ No documents found. Aborting ingestion.\n")
            return
        
        # Chunk documents
        chunks = self.chunk_documents(documents)
        
        # Generate embeddings
        embeddings = self.generate_embeddings(chunks)
        
        # Upload to Qdrant
        self.upload_to_qdrant(chunks, embeddings)
        
        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        print("=" * 60)
        print("✅ INGESTION COMPLETE!")
        print("=" * 60)
        print(f"📊 Statistics:")
        print(f"   Total documents: {len(documents)}")
        print(f"   Total chunks: {len(chunks)}")
        print(f"   Embedding dimension: {self.get_embedding_dimension()}")
        print(f"   Collection: {COLLECTION_NAME}")
        print(f"   Duration: {duration:.2f} seconds")
        print("=" * 60 + "\n")


def main():
    """Main entry point for ingestion script."""
    # Determine docs path (relative to script location)
    script_dir = Path(__file__).parent
    # Go up one level from backend/ to project root, then into docs/
    docs_path = script_dir.parent / "docs"
    
    # Check if --recreate flag is passed
    recreate = "--recreate" in sys.argv
    
    try:
        ingester = MarkdownIngester()
        ingester.ingest(str(docs_path), recreate=recreate)
        
        if recreate:
            print("🎉 Collection recreated and data ingested successfully!")
        else:
            print("🎉 Data ingested successfully!")
            
    except Exception as e:
        print(f"\n❌ Ingestion failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
