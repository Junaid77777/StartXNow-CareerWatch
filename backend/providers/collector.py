import time
from typing import List, Dict, Any, Tuple
from providers.registry import load_providers
from services.logging_service import scheduler_logger, providers_logger
from services.filter_engine import apply_filters
from database import Job, SessionLocal, ProviderHistory, ScanHistory

MAX_RETRIES = 3
RATE_LIMIT_DELAY = 1


def fetch_with_retry(provider, max_retries: int = MAX_RETRIES) -> List[Dict[str, Any]]:
    last_error = None
    for attempt in range(max_retries):
        try:
            jobs = provider.fetch_jobs()
            return jobs, None
        except Exception as e:
            last_error = e
            providers_logger.warning(f"Attempt {attempt + 1} failed for {provider.name}: {str(e)}")
            time.sleep(2)
    providers_logger.error(f"All {max_retries} attempts failed for {provider.name}: {str(last_error)}")
    return [], str(last_error)


def save_provider_history(name: str, status: str, jobs_count: int, error: str = None, duration: float = 0):
    db = SessionLocal()
    try:
        history = ProviderHistory(
            provider_name=name,
            status=status,
            jobs_found=jobs_count,
            error=error,
            duration=f"{duration:.2f}s"
        )
        db.add(history)
        db.commit()
    finally:
        db.close()


def save_scan_history(date: str, jobs_found: int, jobs_added: int, duplicates: int, errors: int, duration: str):
    db = SessionLocal()
    try:
        history = ScanHistory(
            date=date,
            jobs_found=jobs_found,
            jobs_added=jobs_added,
            duplicates=duplicates,
            errors=errors,
            duration=duration
        )
        db.add(history)
        db.commit()
    finally:
        db.close()


def collect_all_jobs() -> Tuple[List[Dict[str, Any]], int, int, int]:
    scheduler_logger.info("Starting job collection from all providers")
    providers = load_providers()
    
    all_jobs = []
    errors = 0
    stats = {"total_time": 0, "provider_times": {}}
    
    for name, provider in providers.items():
        start = time.time()
        time.sleep(RATE_LIMIT_DELAY)
        
        jobs, error = fetch_with_retry(provider)
        elapsed = time.time() - start
        
        if error:
            errors += 1
            save_provider_history(name, "failed", 0, error, elapsed)
        else:
            all_jobs.extend(jobs)
            stats["provider_times"][name] = elapsed
            scheduler_logger.info(f"Collected {len(jobs)} jobs from {name} in {elapsed:.2f}s")
            save_provider_history(name, "success", len(jobs), None, elapsed)
    
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
                source=job.get("source"),
                employment_type=job.get("employment_type"),
                experience=job.get("experience")
            )
            db.add(db_job)
            added += 1
        db.commit()
        scheduler_logger.info(f"Saved {added} jobs to database, skipped {duplicates} duplicates")
    finally:
        db.close()
    return added, duplicates