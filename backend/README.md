# StartXNow Career Watch

Personal job notification bot that monitors company career pages and emails daily reports.

## Version 1

Project foundation with:
- FastAPI application
- SQLite database with SQLAlchemy
- APScheduler with Asia/Kolkata timezone
- Logging configuration
- Configuration via .env

## Setup

```bash
cd backend
pip install -r requirements.txt
```

## Run

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

## Endpoints

- GET /health - Returns status
- POST /scheduler/run-now - Manually trigger scheduler