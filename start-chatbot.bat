@echo off
REM Panaversity RAG Chatbot - Quick Start Script (Windows)
REM This script sets up and runs the entire RAG chatbot system

echo ╔══════════════════════════════════════════════════════════╗
echo ║     PANAVERSITY RAG CHATBOT - QUICK START                ║
echo ║     Physical AI ^& Humanoid Robotics Textbook             ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

REM Check if .env exists
if not exist ".env" (
    echo [ERROR] .env file not found
    echo Please create a .env file with your API keys
    pause
    exit /b 1
)

echo [OK] Found .env file
echo.

REM Step 1: Install backend dependencies
echo [Step 1] Installing backend dependencies...
cd backend

if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

if command -v pip >nul 2>&1 (
    echo Installing Python packages...
    pip install -r requirements.txt
) else (
    echo [ERROR] pip not found. Please install Python.
    pause
    exit /b 1
)

echo [OK] Backend dependencies installed
echo.

REM Step 2: Run ingestion
echo [Step 2] Ingesting textbook content into Qdrant...

if "%1"=="--recreate" (
    echo Recreating collection...
    python ingest.py --recreate
) else (
    python ingest.py
)

if errorlevel 1 (
    echo [ERROR] Ingestion failed
    pause
    exit /b 1
)

echo [OK] Ingestion complete
echo.

REM Step 3: Start backend server in a new window
echo [Step 3] Starting FastAPI backend...
start "Panaversity Backend" cmd /k "cd backend && python main.py"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM Check if backend is running
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Backend is running
) else (
    echo [WARNING] Backend may still be starting...
)

echo.

REM Step 4: Start Docusaurus
echo [Step 4] Starting Docusaurus frontend...
cd ..

if command -v npm >nul 2>&1 (
    echo.
    echo ╔══════════════════════════════════════════════════════════╗
    echo ║     SETUP COMPLETE!                                      ║
    echo ╠══════════════════════════════════════════════════════════╣
    echo ║     Backend: http://localhost:8000                       ║
    echo ║     Frontend: http://localhost:3000                      ║
    echo ║     API Docs: http://localhost:8000/docs                 ║
    echo ║     Chat Widget: Bottom-right corner of the site         ║
    echo ╚══════════════════════════════════════════════════════════╝
    echo.
    echo Starting Docusaurus...
    npm start
) else (
    echo [ERROR] npm not found. Please install Node.js
    taskkill /FI "WINDOWTITLE eq Panaversity Backend"
    exit /b 1
)
