@echo off
REM DNS API Management Platform - Setup Script for Windows

echo.
echo ======================================
echo DNS API Management Platform Setup
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

echo Python and Node.js are installed.
echo.

REM Backend Setup
echo Installing backend dependencies...
cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate.bat

echo Installing Python packages...
pip install -r requirements.txt

if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo !!! IMPORTANT !!!
    echo Please update backend\.env with your credentials:
    echo - NAMECOM_API_KEY
    echo - NAMECOM_API_TOKEN
    echo - NAMECOM_USERNAME
    echo - JWT_SECRET_KEY (change for production)
    echo.
)

cd ..

REM Frontend Setup
echo.
echo Installing frontend dependencies...
cd frontend

call npm install

cd ..

echo.
echo ======================================
echo Setup Complete!
echo ======================================
echo.
echo To start the application:
echo.
echo 1. Backend (PowerShell/CMD):
echo    cd backend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 2. Frontend (new PowerShell/CMD):
echo    cd frontend
echo    npm run dev
echo.
echo Application will be available at:
echo - Frontend: http://localhost:3000
echo - Backend API: http://localhost:8000
echo - API Docs: http://localhost:8000/docs
echo.
echo ======================================
echo.

pause
