from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from dotenv import load_dotenv
import os
import logging

load_dotenv()

SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "Asia/Kolkata")
tz = timezone(SCHEDULER_TIMEZONE)
scheduler = AsyncIOScheduler(timezone=tz)
scheduler_logger = logging.getLogger("scheduler")
_scheduler_running = False


def init_scheduler():
    global _scheduler_running
    if _scheduler_running:
        scheduler_logger.warning("Scheduler already running - preventing duplicate instance")
        return
    
    scheduler_logger.info(f"Initializing scheduler with timezone: {SCHEDULER_TIMEZONE}")
    scheduler.start()
    _scheduler_running = True


async def collect_daily_jobs():
    import time
    from datetime import datetime
    start_time = time.time()
    start_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    scheduler_logger.info(f"=== Daily Job Scan Started at {start_dt} ===")
    
    try:
        from providers.collector import collect_all_jobs, save_jobs_to_db, save_scan_history
        from services.report_service import create_report, update_report
        from services.email_service import send_today_jobs_email
        
        jobs, found, filter_duplicates, errors = collect_all_jobs()
        added, db_duplicates = save_jobs_to_db(jobs)
        
        scheduler_logger.info(f"Jobs scraped: {found}, Added to DB: {added}, Duplicates skipped: {db_duplicates}, Errors: {errors}")
        
        report = create_report(jobs_found=found, new_jobs=added, duplicates=db_duplicates)
        
        email_sent = False
        jobs_emailed = 0
        if added > 0:
            try:
                email_sent = send_today_jobs_email()
                jobs_emailed = added
                scheduler_logger.info(f"Email sent successfully")
            except Exception as e:
                scheduler_logger.error(f"Failed to send email: {str(e)}")
        
        end_time = time.time()
        execution_time = f"{end_time - start_time:.2f}s"
        end_dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        scheduler_logger.info(f"=== Daily Job Scan Completed at {end_dt} ===")
        scheduler_logger.info(f"Execution time: {execution_time}")
        
        update_report(report.id, execution_time, email_sent)
        
        save_scan_history(
            date=datetime.now().strftime("%Y-%m-%d"),
            jobs_found=found,
            jobs_added=added,
            duplicates=db_duplicates,
            errors=errors,
            duration=execution_time
        )
        
        return {
            "jobs_found": found,
            "jobs_added": added,
            "duplicates": db_duplicates,
            "errors": errors,
            "execution_time": execution_time,
            "email_sent": email_sent,
            "jobs_emailed": jobs_emailed,
            "start_time": start_dt,
            "end_time": end_dt
        }
    except Exception as e:
        scheduler_logger.error(f"Scheduler crashed: {str(e)}")
        scheduler_logger.error(f"Daily scan failed - check provider logs")
        return {"jobs_found": 0, "jobs_added": 0, "duplicates": 0, "errors": 1, "execution_time": "0s"}


def add_daily_report_job(hour: int = 19, minute: int = 0):
    scheduler_logger.info(f"Adding daily report job at {hour:02d}:{minute:02d} {SCHEDULER_TIMEZONE}")
    scheduler.add_job(
        collect_daily_jobs,
        trigger=CronTrigger(hour=hour, minute=minute),
        id="daily_report",
        replace_existing=True
    )


def shutdown_scheduler():
    global _scheduler_running
    scheduler_logger.info("Shutting down scheduler")
    scheduler.shutdown()
    _scheduler_running = False