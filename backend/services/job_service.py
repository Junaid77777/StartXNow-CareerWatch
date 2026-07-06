from database import Job, SessionLocal


def get_jobs(skip: int = 0, limit: int = 100):
    db = SessionLocal()
    try:
        return db.query(Job).offset(skip).limit(limit).all()
    finally:
        db.close()


def get_jobs_by_date(date: str):
    db = SessionLocal()
    try:
        from sqlalchemy import func
        return db.query(Job).filter(func.date(Job.created_at) == date).all()
    finally:
        db.close()


def delete_job(job_id: int) -> bool:
    db = SessionLocal()
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            db.delete(job)
            db.commit()
            return True
        return False
    finally:
        db.close()