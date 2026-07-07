@echo off
cd /d D:\Job-alert\backend
call ..\venv\Scripts\activate.bat
python run_daily.py
pause
