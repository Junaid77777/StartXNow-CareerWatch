from fastapi import FastAPI
import config
from database import init_db
from services.scheduler_service import init_scheduler, shutdown_scheduler, collect_daily_jobs, add_daily_report_job
from services.logging_service import scheduler_logger
from services.job_service import get_jobs, delete_job, delete_all_jobs

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
        return {"status": "error", "message": str(e)}


@app.get("/health")
async def health_check():
    return {"status": "running"}


@app.get("/jobs")
async def list_jobs(skip: int = 0, limit: int = 100):
    jobs = get_jobs(skip=skip, limit=limit)
    return {"jobs": [{"id": j.id, "title": j.title, "company": j.company, "location": j.location, "url": j.url, "posted_date": j.posted_date, "source": j.source, "created_at": j.created_at} for j in jobs], "count": len(jobs)}


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
    return {"jobs": [{"id": j.id, "title": j.title, "company": j.company, "location": j.location, "url": j.url, "posted_date": j.posted_date, "source": j.source, "created_at": j.created_at} for j in jobs], "count": len(jobs)}