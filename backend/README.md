# StartXNow Career Watch

Personal job notification bot that monitors 50+ company career pages and emails daily HTML reports.

## Features

- **50+ Company Providers**: Google, Microsoft, Amazon, Adobe, NVIDIA, Intel, Oracle, Cisco, IBM, SAP, Salesforce, ServiceNow, Atlassian, Zoho, Freshworks, Qualcomm, AMD, Accenture, Capgemini, Deloitte, EY, PwC, TCS, Infosys, Wipro, HCL, Tech Mahindra, Cognizant, LTIMindtree, JPMorgan Chase, Goldman Sachs, Morgan Stanley, PhonePe, Razorpay, Flipkart, Swiggy, Meesho, Paytm, Nutanix, Cloudflare, Snowflake, OpenAI, Anthropic, Stripe, Datadog, GitHub, Netflix, Booking.com, Uber, Airbnb
- **Intelligent Filtering**: Accepts software roles, rejects sales/marketing/HR/finance roles, filters by experience and location
- **Production Scheduler**: Runs daily at 7:00 PM IST with retry logic and graceful failure
- **Professional HTML Email**: Responsive daily report with company grouping, badges, and direct apply buttons
- **Health Monitoring**: Health check endpoint for deployment platforms
- **Automatic Log Rotation**: 1MB max with 5 backups

## Installation

```bash
cd backend
pip install -r requirements.txt
copy .env.example .env
```

## Configuration

Edit `config.json` to customize filters:

```json
{
  "filters": {
    "roles": ["Software Engineer", "Software Developer", "Backend Engineer", "Python Developer", "Graduate Engineer"],
    "locations": ["India", "Hyderabad", "Bangalore", "Remote"],
    "experience": ["0-2 Years", "Fresher", "Entry Level"]
  }
}
```

## Environment Variables

Create a `.env` file in the backend directory:

```bash
# Scheduler
SCHEDULER_TIMEZONE=Asia/Kolkata

# Database
DATABASE_PATH=jobs.db

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_TO=recipient@email.com

# Logging
LOGS_DIR=logs
```

## Run Locally

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

The scheduler starts automatically at 7:00 PM IST.

## Deploy

### Railway / Render

1. Connect your repository
2. Set environment variables in the dashboard
3. Deploy the `backend` directory

The app starts automatically via `Procfile`:
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install -r requirements.txt
COPY backend/ .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Scheduler

- Starts automatically on app startup
- Runs daily at 7:00 PM IST (configurable via `add_daily_report_job(hour=19, minute=0)`)
- Prevents duplicate scheduler instances
- Logs start time, end time, jobs scraped, jobs emailed, and errors
- Continues remaining providers if one fails

## Email Setup

For Gmail:
1. Enable 2-factor authentication
2. Generate an App Password
3. Use the App Password as `SMTP_PASSWORD`

For other providers, use the SMTP credentials provided by your email service.

Test email:
```bash
curl -X POST http://localhost:8000/email/test
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Health check for monitoring |
| POST | /scheduler/run-now | Trigger daily scan manually |
| POST | /jobs/refresh | Refresh jobs from all providers |
| GET | /jobs | List all jobs (paginated) |
| GET | /jobs/today | Get jobs from today |
| DELETE | /jobs?job_id=X | Delete a specific job |
| POST | /email/test | Send test email |
| POST | /email/send-today | Send today's jobs via email |
| GET | /reports/latest | Get latest scan report |

## Troubleshooting

- **Email fails**: Verify SMTP credentials in `.env`. For Gmail, use App Password.
- **No jobs found**: Check `logs/scraper.log` for provider errors.
- **Scheduler not running**: Check `logs/scheduler.log` for startup errors.
- **Database issues**: Delete `jobs.db` and restart to reset.
- **Logs not rotating**: Ensure `LOGS_DIR` is writable.

## Testing

```bash
python -m pytest tests/test_filter_engine.py -v
```

## License

MIT