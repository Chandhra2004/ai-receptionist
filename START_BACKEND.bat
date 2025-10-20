@echo off
echo ========================================
echo   Starting Backend Server
echo ========================================
echo.

cd backend
call venv\Scripts\activate
echo Backend server starting...
echo.
echo Open http://localhost:8000 to test API
echo.
python run.py
