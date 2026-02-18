#!/bin/bash
# TalentVector AI - Complete Startup Script for Mac/Linux
# This script starts all three required services

echo ""
echo "========================================"
echo "TalentVector AI - Multi-Service Startup"
echo "========================================"
echo ""

# Check if running Ollama
echo "Checking Ollama service..."
if ! curl -s http://localhost:11434 &> /dev/null; then
    echo ""
    echo "❌ Ollama is NOT running on port 11434"
    echo "Please start Ollama:"
    echo "  1. Open Terminal"
    echo "  2. Run: ollama serve"
    echo ""
    read -p "Press Enter to continue..."
else
    echo "✓ Ollama is running"
fi

# Check if backend is already running
echo ""
echo "Checking backend service..."
if ! curl -s http://localhost:8000/health &> /dev/null; then
    echo "✓ Starting Backend on port 8000..."
    cd talentvector
    python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000 &
    BACKEND_PID=$!
    cd ..
    sleep 3
else
    echo "✓ Backend already running on port 8000"
fi

# Check if frontend is already running
echo ""
echo "Checking frontend service..."
if ! curl -s http://localhost:5173 &> /dev/null; then
    echo "✓ Starting Frontend on port 5173..."
    cd talentvector/frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ../..
    sleep 3
else
    echo "✓ Frontend already running on port 5173"
fi

echo ""
echo "========================================"
echo "All services are now running!"
echo "========================================"
echo ""
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Open your browser and navigate to:"
echo "http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for all background processes
wait
