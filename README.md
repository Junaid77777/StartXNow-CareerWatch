# 🚀 StartXNow Career Watch

An automated Python-based job intelligence system that monitors **official Indian company career pages**, filters **entry-level software jobs**, removes duplicates, and sends a **daily HTML email report** automatically using GitHub Actions.

---

## ✨ Features

- ✅ Scrapes jobs from official company career pages
- 🇮🇳 Filters only India-based opportunities
- 👨‍💻 Filters Software & IT roles
- 🎓 Keeps only Fresher / Entry-Level jobs
- 🚫 Removes duplicate job postings
- 📧 Sends a professional HTML email report
- ⏰ Runs automatically every day using GitHub Actions
- 🗃 Stores job history in SQLite
- 📝 Generates execution logs
- 🔒 Uses GitHub Secrets for secure credentials

---

# Tech Stack

- Python 3.12
- FastAPI
- SQLite
- APScheduler
- Jinja2
- SMTP (Gmail)
- GitHub Actions
- BeautifulSoup
- Requests

---

# Project Structure

```
backend/
│
├── providers/
│   ├── google.py
│   ├── microsoft.py
│   ├── amazon.py
│   ├── adobe.py
│   ├── ...
│
├── services/
│   ├── email_service.py
│   ├── scheduler_service.py
│   ├── filter_engine.py
│   ├── job_service.py
│   └── report_service.py
│
├── database.py
├── main.py
├── run_daily.py
├── requirements.txt
│
.github/
└── workflows/
    └── daily-career-watch.yml
```

---

# Workflow

```
Official Company Career Pages
            │
            ▼
      Collect Jobs
            │
            ▼
   Normalize Job Data
            │
            ▼
 Remove Duplicate Jobs
            │
            ▼
 Filter Indian Software Jobs
            │
            ▼
 Generate HTML Report
            │
            ▼
 Send Email
            │
            ▼
 GitHub Actions (Daily)
```

---

# Filtering Rules

### Location

Only jobs located in India:

- Bangalore
- Hyderabad
- Pune
- Chennai
- Mumbai
- Noida
- Gurugram
- Delhi
- Ahmedabad
- Coimbatore
- Kochi
- Kolkata
- Remote (India)

---

### Experience

Accepts:

- Fresher
- Entry Level
- Associate
- Graduate
- Campus Hiring
- 0–2 Years

Rejects:

- Senior
- Lead
- Principal
- Architect
- Director
- Manager

---

### Roles

Accepts:

- Software Engineer
- Software Developer
- Backend Engineer
- Python Developer
- Full Stack Developer
- SDE
- Data Engineer
- Data Scientist
- AI Engineer
- ML Engineer
- DevOps Engineer

---

# Automation

The project executes automatically every day using GitHub Actions.

Pipeline:

1. Checkout Repository
2. Install Dependencies
3. Scrape Company Career Pages
4. Filter Jobs
5. Remove Duplicates
6. Generate HTML Email
7. Send Daily Report

---

# Security

Sensitive credentials are stored securely using GitHub Secrets.

Required Secrets:

- SMTP_USER
- SMTP_PASSWORD
- EMAIL_TO

No credentials are committed to the repository.

---

# Future Improvements

- AI Job Ranking
- Resume Matching
- Salary Prediction
- Telegram Notifications
- WhatsApp Notifications
- Web Dashboard
- Docker Support
- Unit Testing
- Analytics Dashboard

---

# Author

**Shaik Junaid**

B.Tech Computer Science & Engineering

India 🇮🇳

---

# License

This project is intended for educational and personal use.
