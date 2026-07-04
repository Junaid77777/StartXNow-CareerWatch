from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from dotenv import load_dotenv
import os

load_dotenv()

SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "Asia/Kolkata")
tz = timezone(SCHEDULER_TIMEZONE)
scheduler = AsyncIOScheduler(timezone=tz)

import logging
scheduler_logger = logging.getLogger("scheduler")


def init_scheduler():
    scheduler_logger.info(f"Initializing scheduler with timezone: {SCHEDULER_TIMEZONE}")
    scheduler.start()


async def collect_daily_jobs():
    scheduler_logger.info("Running Daily Scan")
    from providers.collector import collect_all_jobs, save_jobs_to_db
    jobs, found, filter_duplicates, errors = collect_all_jobs()
    added, db_duplicates = save_jobs_to_db(jobs)
    return {"jobs_found": found, "jobs_added": added, "duplicates": db_duplicates, "errors": errors}


def add_daily_report_job(hour: int = 19, minute: int = 0):
    scheduler_logger.info(f"Adding daily report job at {hour:02d}:{minute:02d}")
    scheduler.add_job(
        collect_daily_jobs,
        trigger=CronTrigger(hour=hour, minute=minute),
        id="daily_report",
        replace_existing=True
    )


def shutdown_scheduler():
    scheduler_logger.info("Shutting down scheduler")
    scheduler.shutdown()