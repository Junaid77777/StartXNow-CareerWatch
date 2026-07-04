import os
from dotenv import load_dotenv

load_dotenv()

SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "Asia/Kolkata")
DATABASE_PATH = os.getenv("DATABASE_PATH", "jobs.db")
LOGS_DIR = os.getenv("LOGS_DIR", "logs")

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_TO = os.getenv("EMAIL_TO", "")