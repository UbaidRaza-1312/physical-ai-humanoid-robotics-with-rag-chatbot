#!/bin/bash
# Panaversity RAG Chatbot - Quick Start Script
# This script sets up and runs the entire RAG chatbot system

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     PANAVERSITY RAG CHATBOT - QUICK START                ║"
echo "║     Physical AI & Humanoid Robotics Textbook             ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ Error: .env file not found${NC}"
    echo "Please create a .env file with your API keys"
    exit 1
fi

echo -e "${GREEN}✅ Found .env file${NC}"

# Step 1: Install backend dependencies
echo -e "\n${BLUE}📦 Step 1: Installing backend dependencies...${NC}"
cd backend

if command -v uv &> /dev/null; then
    echo "Using uv for installation..."
    uv pip install -r requirements.txt
elif command -v pip &> /dev/null; then
    echo "Using pip for installation..."
    pip install -r requirements.txt
else
    echo -e "${RED}❌ No Python package manager found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Backend dependencies installed${NC}"

# Step 2: Run ingestion
echo -e "\n${BLUE}📚 Step 2: Ingesting textbook content into Qdrant...${NC}"

if [ "$1" == "--recreate" ]; then
    echo "Recreating collection..."
    python ingest.py --recreate
else
    python ingest.py
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Ingestion failed${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Ingestion complete${NC}"

# Step 3: Start backend server
echo -e "\n${BLUE}🚀 Step 3: Starting FastAPI backend...${NC}"
echo -e "${YELLOW}Backend will start at http://localhost:8000${NC}"
echo -e "${YELLOW}API docs at http://localhost:8000/docs${NC}"
echo ""
echo -e "${BLUE}Starting server...${NC}"
python main.py &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to initialize..."
sleep 3

# Check if backend is running
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend is running${NC}"
else
    echo -e "${YELLOW}⚠️  Backend may still be starting...${NC}"
fi

# Step 4: Start Docusaurus
echo -e "\n${BLUE}🌐 Step 4: Starting Docusaurus frontend...${NC}"
cd ..

if command -v npm &> /dev/null; then
    echo -e "${YELLOW}Frontend will start at http://localhost:3000${NC}"
    echo ""
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     ✅ SETUP COMPLETE!                                   ║${NC}"
    echo -e "${GREEN}╠══════════════════════════════════════════════════════════╣${NC}"
    echo -e "${GREEN}║     Backend: http://localhost:8000                       ║${NC}"
    echo -e "${GREEN}║     Frontend: http://localhost:3000                      ║${NC}"
    echo -e "${GREEN}║     API Docs: http://localhost:8000/docs                 ║${NC}"
    echo -e "${GREEN}║     Chat Widget: Bottom-right corner of the site         ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${BLUE}Starting Docusaurus...${NC}"
    npm start
else
    echo -e "${RED}❌ npm not found. Please install Node.js${NC}"
    kill $BACKEND_PID
    exit 1
fi

# Cleanup on exit
trap "echo '\nStopping backend...'; kill $BACKEND_PID" EXIT
