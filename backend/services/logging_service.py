import logging
import os
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv

load_dotenv()

LOGS_DIR = os.getenv("LOGS_DIR", "logs")

os.makedirs(LOGS_DIR, exist_ok=True)


def setup_logger(name: str, log_file: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        file_handler = RotatingFileHandler(
            os.path.join(LOGS_DIR, log_file),
            maxBytes=1024*1024,
            backupCount=5
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        logger.addHandler(file_handler)
    
    return logger


scheduler_logger = setup_logger("scheduler", "scheduler.log")
providers_logger = setup_logger("providers", "providers.log")
email_logger = setup_logger("email", "email.log")