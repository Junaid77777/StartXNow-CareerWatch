import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

LOGS_DIR = os.getenv("LOGS_DIR", "logs")

os.makedirs(LOGS_DIR, exist_ok=True)


class JobStatsFormatter(logging.Formatter):
    def format(self, record):
        msg = super().format(record)
        extras = []
        if hasattr(record, 'company'):
            extras.append(f"Company: {record.company}")
        if hasattr(record, 'duration'):
            extras.append(f"Duration: {record.duration}s")
        if hasattr(record, 'status'):
            extras.append(f"Status: {record.status}")
        if hasattr(record, 'errors'):
            extras.append(f"Errors: {record.errors}")
        extras.append(f"Jobs: {getattr(record, 'jobs', '')}")
        if extras:
            msg += " | " + " | ".join(extras)
        return msg


def setup_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            os.path.join(LOGS_DIR, log_file),
            maxBytes=1024*1024,
            backupCount=5
        )
        file_handler.setFormatter(JobStatsFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)
    
    return logger


scheduler_logger = setup_logger("scheduler", "scheduler.log")
providers_logger = setup_logger("providers", "scraper.log")
email_logger = setup_logger("email", "email.log")