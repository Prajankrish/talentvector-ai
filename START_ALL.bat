@echo off
REM TalentVector AI - Complete Startup Script for Windows
REM This script starts all three required services

echo.
echo ========================================
echo TalentVector AI - Multi-Service Startup
echo ========================================
echo.

REM Check if running Ollama
echo Checking Ollama service...
curl -s http://localhost:11434 >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Ollama is NOT running on port 11434
    echo Please start Ollama:
    echo   1. Open Command Prompt
    echo   2. Run: ollama serve
    echo.
    pause
) else (
    echo ✓ Ollama is running
)

REM Check if backend is already running
echo.
echo Checking backend service...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ✓ Starting Backend on port 8000...
    start cmd /k "cd talentvector && python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000"
    timeout /t 3 /nobreak
) else (
    echo ✓ Backend already running on port 8000
)

REM Check if frontend is already running
echo.
echo Checking frontend service...
curl -s http://localhost:5173 >nul 2>&1
if %errorlevel% neq 0 (
    echo ✓ Starting Frontend on port 5173...
    start cmd /k "cd talentvector\frontend && npm run dev"
    timeout /t 3 /nobreak
) else (
    echo ✓ Frontend already running on port 5173
)

echo.
echo ========================================
echo All services are now running!
echo ========================================
echo.
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Open your browser and navigate to:
echo http://localhost:5173
echo.
pause
