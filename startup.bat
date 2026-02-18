@echo off
REM TalentVector AI - Complete Project Startup Script for Windows

echo ============================================================
echo   TalentVector AI - Complete Startup
echo ============================================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call .\venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt > nul 2>&1

REM Create data directory
if not exist "data" (
    mkdir data
)

echo.
echo ============================================================
echo  Startup Complete!
echo ============================================================
echo.
echo To run the project in separate terminals:
echo.
echo Terminal 1 (Backend):
echo   cd backend
echo   python main.py
echo.
echo Terminal 2 (Frontend):
echo   streamlit run app.py
echo.
echo Frontend will open at: http://localhost:8501
echo Backend API at: http://localhost:8000
echo API Docs at: http://localhost:8000/docs
echo.
echo ============================================================
pause
