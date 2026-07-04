from typing import List, Dict, Any, Tuple
from providers.registry import load_providers
from services.logging_service import scheduler_logger
from services.filter_service import apply_filters
from database import Job, SessionLocal


def collect_all_jobs() -> Tuple[List[Dict[str, Any]], int, int, int]:
    scheduler_logger.info("Starting job collection from all providers")
    providers = load_providers()
    
    all_jobs = []
    errors = 0
    
    for name, provider in providers.items():
        try:
            jobs = provider.fetch_jobs()
            all_jobs.extend(jobs)
            scheduler_logger.info(f"Collected {len(jobs)} jobs from {name}")
        except Exception as e:
            scheduler_logger.error(f"Error fetching jobs from {name}: {str(e)}")
            errors += 1
    
    scheduler_logger.info(f"Total jobs collected: {len(all_jobs)}")
    
    filtered_jobs = apply_filters(all_jobs)
    duplicates = len(all_jobs) - len(filtered_jobs)
    
    scheduler_logger.info(f"After filtering: {len(filtered_jobs)} jobs matched")
    return filtered_jobs, len(all_jobs), duplicates, errors


def save_jobs_to_db(jobs: List[Dict[str, Any]]) -> Tuple[int, int]:
    from datetime import datetime
    db = SessionLocal()
    added = 0
    duplicates = 0
    try:
        for job in jobs:
            existing = db.query(Job).filter(Job.url == job.get("url")).first()
            if existing:
                duplicates += 1
                continue
            db_job = Job(
                title=job["title"],
                company=job.get("company"),
                location=job.get("location"),
                url=job.get("url"),
                posted_date=job.get("posted_date") or datetime.now().strftime("%Y-%m-%d"),
                source=job.get("source")
            )
            db.add(db_job)
            added += 1
        db.commit()
        scheduler_logger.info(f"Saved {added} jobs to database, skipped {duplicates} duplicates")
    finally:
        db.close()
    return added, duplicates