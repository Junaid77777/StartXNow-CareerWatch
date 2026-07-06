from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = os.getenv("DATABASE_PATH", "jobs.db")
engine = create_engine(f"sqlite:///{DATABASE_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String)
    location = Column(String)
    url = Column(String)
    description = Column(Text)
    posted_date = Column(String)
    source = Column(String)
    employment_type = Column(String)
    experience = Column(String)
    is_new = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Provider(Base):
    __tablename__ = "providers"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    base_url = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DailyReport(Base):
    __tablename__ = "daily_reports"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    scan_time = Column(String)
    jobs_found = Column(Integer, default=0)
    new_jobs = Column(Integer, default=0)
    duplicates = Column(Integer, default=0)
    execution_time = Column(String)
    email_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ProviderHistory(Base):
    __tablename__ = "provider_history"
    
    id = Column(Integer, primary_key=True, index=True)
    provider_name = Column(String, nullable=False)
    status = Column(String, nullable=False)
    jobs_found = Column(Integer, default=0)
    error = Column(Text)
    duration = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class ScanHistory(Base):
    __tablename__ = "scan_history"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(String, nullable=False)
    jobs_found = Column(Integer, default=0)
    jobs_added = Column(Integer, default=0)
    duplicates = Column(Integer, default=0)
    errors = Column(Integer, default=0)
    duration = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


def init_db():
    Base.metadata.create_all(bind=engine)