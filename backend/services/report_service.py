from sqlalchemy.orm import Session
from database import DailyReport, SessionLocal
from datetime import datetime
import time


def create_report(jobs_found: int, new_jobs: int, duplicates: int, email_sent: bool = False) -> DailyReport:
    db = SessionLocal()
    try:
        report = DailyReport(
            date=datetime.now().strftime("%Y-%m-%d"),
            scan_time=datetime.now().strftime("%H:%M:%S"),
            jobs_found=jobs_found,
            new_jobs=new_jobs,
            duplicates=duplicates,
            execution_time="",
            email_sent=email_sent
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report
    finally:
        db.close()


def update_report(report_id: int, execution_time: str, email_sent: bool = True):
    db = SessionLocal()
    try:
        report = db.query(DailyReport).filter(DailyReport.id == report_id).first()
        if report:
            report.execution_time = execution_time
            report.email_sent = email_sent
            db.commit()
    finally:
        db.close()


def get_latest_report():
    db = SessionLocal()
    try:
        return db.query(DailyReport).order_by(DailyReport.id.desc()).first()
    finally:
        db.close()