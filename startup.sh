#!/bin/bash
# TalentVector AI - Complete Project Startup Script for Linux/Mac

echo "==========================================================="
echo "  TalentVector AI - Complete Startup (Linux/Mac)"
echo "==========================================================="
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install requirements
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Create data directory
mkdir -p data

echo ""
echo "==========================================================="
echo "  Startup Complete!"
echo "==========================================================="
echo ""
echo "To run the project in separate terminals:"
echo ""
echo "Terminal 1 (Backend):"
echo "  cd backend"
echo "  python main.py"
echo ""
echo "Terminal 2 (Frontend):"
echo "  streamlit run app.py"
echo ""
echo "Frontend will open at: http://localhost:8501"
echo "Backend API at: http://localhost:8000"
echo "API Docs at: http://localhost:8000/docs"
echo ""
echo "==========================================================="
