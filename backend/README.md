# StartXNow Career Watch

Personal job notification bot that monitors company career pages and emails daily reports.

## Architecture

```
StartXNow-CareerWatch/
├── backend/
│   ├── providers/
│   │   ├── base.py              # Base provider class
│   │   ├── registry.py          # Dynamic provider loader
│   │   ├── collector.py         # Job collection orchestration
│   │   ├── google.py            # Google provider
│   │   ├── microsoft.py         # Microsoft provider
│   │   ├── amazon.py            # Amazon provider
│   │   ├── oracle.py            # Oracle provider
│   │   ├── accenture.py         # Accenture provider
│   │   └── ibm.py               # IBM provider
│   ├── services/
│   │   ├── scheduler_service.py   # APScheduler setup
│   │   ├── logging_service.py     # Logging configuration
│   │   ├── job_service.py         # Job CRUD operations
│   │   ├── email_service.py       # SMTP email service
│   │   ├── filter_service.py      # Job filtering logic
│   │   └── report_service.py      # Report management
│   ├── templates/
│   │   └── __init__.py
│   ├── logs/
│   │   ├── scheduler.log
│   │   ├── providers.log
│   │   └── email.log
│   ├── database.py              # SQLAlchemy models
│   ├── config.py                # Configuration loader
│   ├── config.json              # Provider and filter config
│   ├── main.py                  # FastAPI application
│   ├── requirements.txt         # Python dependencies
│   └── .env.example             # Environment template
```

## Installation

```bash
# Clone the repository
cd StartXNow-CareerWatch/backend

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Edit .env with your credentials
# SMTP_USER=your-email@gmail.com
# SMTP_PASSWORD=your-app-password
# EMAIL_TO=your-email@gmail.com
```

## Running

```bash
# Start the server
uvicorn main:app --host 127.0.0.1 --port 8000

# Or for development with auto-reload
uvicorn main:app --reload
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check |
| POST | /scheduler/run-now | Trigger daily scan manually |
| POST | /jobs/refresh | Refresh jobs from all providers |
| GET | /jobs | List all jobs |
| GET | /jobs/today | Get jobs from today |
| DELETE | /jobs?job_id=X | Delete a specific job |
| POST | /email/test | Send test email |
| GET | /reports/latest | Get latest scan report |

## Configuration

Edit `config.json`:

```json
{
  "filters": {
    "roles": ["Software Engineer", "Software Developer", "Backend Engineer", "Python Developer", "Graduate Engineer"],
    "locations": ["India", "Hyderabad", "Bangalore", "Remote"],
    "experience": ["0-2 Years", "Fresher", "Entry Level"]
  },
  "companies": [
    {"name": "google", "module": "providers.google", "base_url": "https://careers.google.com"},
    ...
  ]
}
```

## Troubleshooting

**Email fails to send:**
- Verify SMTP credentials in `.env` file
- For Gmail, use App Password instead of regular password
- Check `logs/email.log` for error details

**No jobs found:**
- Check `logs/providers.log` for provider loading errors
- Verify providers return jobs matching your filters in `config.json`
- Check `logs/scheduler.log` for collection errors

**Scheduler not running:**
- Verify `SCHEDULER_TIMEZONE` in `.env` matches your timezone
- Check that the daily job is added at startup in logs

**Database issues:**
- Delete `jobs.db` to reset the database (loses all data)
- Restart the server to recreate tables