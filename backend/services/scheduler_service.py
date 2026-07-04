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
    import time
    start_time = time.time()
    scheduler_logger.info("Running Daily Scan")
    
    try:
        from providers.collector import collect_all_jobs, save_jobs_to_db
        from services.report_service import create_report, update_report
        
        jobs, found, filter_duplicates, errors = collect_all_jobs()
        added, db_duplicates = save_jobs_to_db(jobs)
        
        report = create_report(jobs_found=found, new_jobs=added, duplicates=db_duplicates)
        
        email_sent = False
        if added > 0:
            try:
                from services.email_service import send_email, render_job_report_template
                from services.job_service import get_jobs
                all_jobs = get_jobs()
                html_content = render_job_report_template([
                    {"company": j.company, "title": j.title, "location": j.location, "url": j.url}
                    for j in all_jobs
                ])
                email_sent = send_email("StartXNow Career Watch", html_content)
            except Exception as e:
                scheduler_logger.error(f"Failed to send email: {str(e)}")
        
        execution_time = f"{time.time() - start_time:.2f}s"
        update_report(report.id, execution_time, email_sent)
        
        return {"jobs_found": found, "jobs_added": added, "duplicates": db_duplicates, "errors": errors, "execution_time": execution_time}
    except Exception as e:
        scheduler_logger.error(f"Scheduler crashed: {str(e)}")
        return {"jobs_found": 0, "jobs_added": 0, "duplicates": 0, "errors": 1, "execution_time": "0s"}


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