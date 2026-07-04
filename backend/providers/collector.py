import time
from typing import List, Dict, Any, Tuple
from providers.registry import load_providers
from services.logging_service import scheduler_logger, providers_logger
from services.filter_service import apply_filters
from database import Job, SessionLocal

MAX_RETRIES = 3
PROVIDER_TIMEOUT = 30


def fetch_with_retry(provider, max_retries: int = MAX_RETRIES) -> List[Dict[str, Any]]:
    last_error = None
    for attempt in range(max_retries):
        try:
            jobs = provider.fetch_jobs()
            return jobs
        except Exception as e:
            last_error = e
            providers_logger.warning(f"Attempt {attempt + 1} failed for {provider.name}: {str(e)}")
            time.sleep(2)
    providers_logger.error(f"All {max_retries} attempts failed for {provider.name}: {str(last_error)}")
    return []


def collect_all_jobs() -> Tuple[List[Dict[str, Any]], int, int, int]:
    scheduler_logger.info("Starting job collection from all providers")
    providers = load_providers()
    
    all_jobs = []
    errors = 0
    stats = {"total_time": 0, "provider_times": {}}
    
    for name, provider in providers.items():
        start = time.time()
        try:
            jobs = fetch_with_retry(provider)
            all_jobs.extend(jobs)
            elapsed = time.time() - start
            stats["provider_times"][name] = elapsed
            scheduler_logger.info(f"Collected {len(jobs)} jobs from {name} in {elapsed:.2f}s")
        except Exception as e:
            scheduler_logger.error(f"Error fetching jobs from {name}: {str(e)}")
            errors += 1
    
    stats["total_time"] = sum(stats["provider_times"].values())
    scheduler_logger.info(f"Total jobs collected: {len(all_jobs)} in {stats['total_time']:.2f}s")
    
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