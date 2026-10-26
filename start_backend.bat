@echo off
echo ========================================================
echo Starting BIS AI Copilot Backend (FastAPI on Port 8000)...
echo ========================================================
cd /d "%~dp0"
"%~dp0backend\venv\Scripts\python.exe" -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
pause
