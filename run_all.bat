@echo off
echo ========================================================
echo Launching BIS AI Copilot (Full Stack)...
echo ========================================================
start "BIS AI Copilot Backend (FastAPI)" cmd /c "%~dp0start_backend.bat"
timeout /t 3 /nobreak >nul
start "BIS AI Copilot Frontend (Next.js)" cmd /c "%~dp0start_frontend.bat"
echo.
echo Both services are starting:
echo  - Backend API: http://127.0.0.1:8000
echo  - Interactive Swagger Docs: http://127.0.0.1:8000/docs
echo  - Web Application: http://localhost:3000
echo.
echo You can now navigate to http://localhost:3000 in your browser.
pause
