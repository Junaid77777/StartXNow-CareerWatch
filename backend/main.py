from fastapi import FastAPI
from database import init_db
from services.scheduler_service import init_scheduler, shutdown_scheduler, collect_daily_jobs, add_daily_report_job
from services.logging_service import scheduler_logger
from services.job_service import get_jobs, delete_job

app = FastAPI(title="StartXNow Career Watch")


@app.on_event("startup")
async def startup_event():
    init_db()
    init_scheduler()
    add_daily_report_job(hour=19, minute=0)


@app.on_event("shutdown")
async def shutdown_event():
    shutdown_scheduler()


@app.post("/scheduler/run-now")
async def run_scheduler_now():
    scheduler_logger.info("Manual trigger received for /scheduler/run-now")
    try:
        result = await collect_daily_jobs()
        return {"status": "success", "result": result}
    except Exception as e:
        scheduler_logger.error(f"Error running scheduler: {str(e)}")
        return {"status": "error", "message": str(e), "stack": str(e)}


@app.get("/health")
async def health_check():
    return {"status": "running"}


@app.get("/jobs")
async def list_jobs(skip: int = 0, limit: int = 100):
    jobs = get_jobs(skip=skip, limit=limit)
    return {"jobs": [{"id": j.id, "title": j.title, "company": j.company, "location": j.location, "url": j.url, "posted_date": j.posted_date, "source": j.source, "employment_type": j.employment_type, "experience": j.experience, "created_at": j.created_at} for j in jobs], "count": len(jobs)}


@app.delete("/jobs")
async def remove_job(job_id: int):
    deleted = delete_job(job_id)
    if deleted:
        return {"status": "deleted", "id": job_id}
    return {"status": "not_found", "id": job_id}


@app.post("/jobs/refresh")
async def refresh_jobs():
    scheduler_logger.info("Manual job refresh triggered")
    try:
        result = await collect_daily_jobs()
        return {
            "jobs_found": result.get("jobs_found", 0),
            "jobs_added": result.get("jobs_added", 0),
            "duplicates": result.get("duplicates", 0),
            "errors": result.get("errors", 0)
        }
    except Exception as e:
        scheduler_logger.error(f"Error refreshing jobs: {str(e)}")
        return {"error": str(e)}


@app.get("/jobs/today")
async def get_todays_jobs():
    from services.job_service import get_jobs_by_date
    from datetime import datetime
    jobs = get_jobs_by_date(datetime.now().strftime("%Y-%m-%d"))
    return {"jobs": [{"id": j.id, "title": j.title, "company": j.company, "location": j.location, "url": j.url, "posted_date": j.posted_date, "source": j.source, "employment_type": j.employment_type, "experience": j.experience, "created_at": j.created_at} for j in jobs], "count": len(jobs)}


@app.post("/email/test")
async def test_email():
    from services.email_service import send_email, render_job_report_template, SMTP_USER, SMTP_PASSWORD
    from services.logging_service import email_logger
    
    if not SMTP_USER or not SMTP_PASSWORD:
        return {"status": "error", "message": "Email credentials not configured in .env"}
    
    try:
        html_content = render_job_report_template([
            {"company": "Google", "title": "Software Engineer", "location": "Bangalore, India", "url": "https://careers.google.com/jobs/123", "posted_date": "2026-07-06", "employment_type": "Full-time", "experience": "Entry Level"},
            {"company": "Microsoft", "title": "Python Developer", "location": "Hyderabad, India", "url": "https://careers.microsoft.com/jobs/456", "posted_date": "2026-07-05", "employment_type": "Full-time", "experience": "0-2 Years"}
        ])
        success = send_email("StartXNow AI Daily Career Report - Test", html_content)
        if success:
            return {"status": "success", "message": "Test email sent"}
        return {"status": "error", "message": "Failed to send email - check logs"}
    except Exception as e:
        email_logger.error(f"Email test failed: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.post("/email/send-today")
async def send_today_email():
    from services.email_service import send_today_jobs_email
    from services.logging_service import email_logger
    
    try:
        success = send_today_jobs_email()
        if success:
            email_logger.info("Today's jobs email sent successfully")
            return {"status": "success", "message": "Email sent with today's jobs"}
        email_logger.error("Failed to send today's jobs email")
        return {"status": "error", "message": "Failed to send email - check logs"}
    except Exception as e:
        email_logger.error(f"Send today email failed: {str(e)}")
        return {"status": "error", "message": str(e)}


@app.get("/reports/latest")
async def get_latest_report():
    from services.report_service import get_latest_report
    report = get_latest_report()
    if report:
        return {
            "date": report.date,
            "scan_time": report.scan_time,
            "jobs_found": report.jobs_found,
            "new_jobs": report.new_jobs,
            "duplicates": report.duplicates,
            "execution_time": report.execution_time,
            "email_sent": report.email_sent
        }
    return {"message": "No reports found"}