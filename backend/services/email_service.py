import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from jinja2 import Template
from datetime import datetime
from collections import defaultdict
from services.filter_engine import job_is_fresher

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_TO = os.getenv("EMAIL_TO", "")


def send_email(subject: str, html_content: str) -> bool:
    if not SMTP_USER or not SMTP_PASSWORD:
        from services.logging_service import email_logger
        email_logger.error("Email credentials not configured")
        return False
    
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = SMTP_USER
        msg["To"] = EMAIL_TO
        
        msg.attach(MIMEText(html_content, "html"))
        
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, EMAIL_TO, msg.as_string())
        
        from services.logging_service import email_logger
        email_logger.info(f"Email sent to {EMAIL_TO}")
        return True
    except Exception as e:
        import traceback
        traceback.print_exc()

        from services.logging_service import email_logger
        email_logger.exception("Failed to send email")

        raise


def is_remote(job: dict) -> bool:
    location = str(job.get("location", "")).lower()
    return "remote" in location


def is_hybrid(job: dict) -> bool:
    employment_type = str(job.get("employment_type", "")).lower()
    return "hybrid" in employment_type


def render_job_report_template(jobs: list, total_count: int = 0, scan_stats: dict = None) -> str:
    template = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container { 
            max-width: 700px; 
            margin: 0 auto; 
            background: #ffffff; 
            padding: 0; 
            border-radius: 12px; 
            box-shadow: 0 10px 40px rgba(0,0,0,0.15);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #1a73e8 0%, #0d47a1 100%);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 28px;
            font-weight: 700;
        }
        .header .date {
            margin-top: 8px;
            font-size: 14px;
            opacity: 0.9;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 10px;
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }
        .stat-card {
            background: #ffffff;
            border-radius: 8px;
            padding: 12px 14px;
            text-align: center;
            border: 1px solid #e9ecef;
        }
        .stat-value {
            font-size: 22px;
            font-weight: 700;
            color: #1a73e8;
        }
        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 4px;
        }
        .company-group {
            margin: 0 20px 20px;
        }
        .company-name {
            background: #f1f3f4;
            padding: 12px 16px;
            font-weight: 600;
            color: #1a73e8;
            font-size: 16px;
            border-radius: 6px 6px 0 0;
            border-left: 4px solid #1a73e8;
        }
        .job {
            padding: 16px;
            border-bottom: 1px solid #e9ecef;
            border-left: 1px solid #e9ecef;
            border-right: 1px solid #e9ecef;
        }
        .job:first-child {
            border-top: 1px solid #e9ecef;
            border-radius: 0 0 0 0;
        }
        .job:last-child {
            border-radius: 0 0 6px 6px;
        }
        .job-title {
            font-size: 16px;
            font-weight: 600;
            color: #212529;
            margin-bottom: 8px;
        }
        .job-meta {
            font-size: 13px;
            color: #868e96;
            margin-bottom: 4px;
        }
        .job-badges {
            margin-top: 8px;
            margin-bottom: 10px;
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
            margin-right: 8px;
        }
        .badge-remote { background: #e8f5e9; color: #2e7d32; }
        .badge-hybrid { background: #e3f2fd; color: #1565c0; }
        .badge-entry { background: #fff3e0; color: #ef6c00; }
        .apply-btn {
            display: inline-block;
            background: #1a73e8;
            color: white !important;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            margin-top: 10px;
        }
        .apply-btn:hover { background: #0d47a1; }
        .no-jobs {
            text-align: center;
            padding: 60px 20px;
            color: #6c757d;
        }
        .no-jobs h3 {
            margin: 0 0 12px;
            color: #495057;
        }
        .footer {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #adb5bd;
            font-size: 12px;
        }
        @media (max-width: 600px) {
            body { padding: 10px; }
            .container { border-radius: 8px; }
            .header { padding: 20px 15px; }
            .header h1 { font-size: 22px; }
            .company-group { margin: 0 15px 15px; }
            .job { padding: 12px; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🇮🇳 StartXNow Career Watch</h1>
            <div class="date">{{ current_date }}</div>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{{ stats.companies_scanned }}</div>
                <div class="stat-label">Companies Scanned</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ stats.jobs_found }}</div>
                <div class="stat-label">Jobs Found</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ stats.indian_jobs_matched }}</div>
                <div class="stat-label">Indian Jobs Matched</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ stats.duplicates_removed }}</div>
                <div class="stat-label">Duplicates Removed</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ stats.providers_failed }}</div>
                <div class="stat-label">Providers Failed</div>
            </div>
        </div>
        
        {% if jobs %}
            {% for company, company_jobs in jobs_by_company.items() %}
            <div class="company-group">
                <div class="company-name">{{ company }} ({{ company_jobs|length }} position{{ 's' if company_jobs|length > 1 else '' }})</div>
                {% for job in company_jobs %}
                <div class="job">
                    <div class="job-title">💼 {{ job.title }}</div>
                    <div class="job-meta">📍 {{ job.location }}</div>
                    <div class="job-meta">🎓 {{ job.experience or 'Not specified' }}</div>
                    <div class="job-meta">📅 {{ job.posted_date or 'Date not specified' }}</div>
                    <div class="job-badges">
                        {% if job.is_remote %}<span class="badge badge-remote">Remote</span>{% endif %}
                        {% if job.is_hybrid %}<span class="badge badge-hybrid">Hybrid</span>{% endif %}
                        {% if job.is_entry_level %}<span class="badge badge-entry">Entry Level</span>{% endif %}
                    </div>
                    <a href="{{ job.url }}" class="apply-btn" target="_blank" rel="noopener noreferrer">🔗 Apply Now</a>
                </div>
                {% endfor %}
            </div>
            {% endfor %}
        {% else %}
            <div class="no-jobs">
                <h3>No new matching jobs were found today.</h3>
                <p>Check back tomorrow for fresh opportunities!</p>
            </div>
        {% endif %}
        
        <div class="footer">
            Generated by StartXNow Career Watch • {{ current_date }}
        </div>
    </div>
</body>
</html>
""")
    
    seen = set()
    unique_jobs = []
    for job in jobs:
        company = str(job.get("company", "") or "")
        title = str(job.get("title", "") or "")
        url = str(job.get("url", "") or "")
        key = (company, title, url)
        if key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    def sort_key(job):
        posted = job.get("posted_date") or ""
        return (not posted, posted)
    
    unique_jobs.sort(key=sort_key)
    
    jobs_by_company = defaultdict(list)
    for job in unique_jobs:
        company = job.get("company", "Unknown") or "Unknown"
        job_copy = dict(job)
        job_copy["is_remote"] = is_remote(job)
        job_copy["is_hybrid"] = is_hybrid(job)
        job_copy["is_entry_level"] = job_is_fresher(job.get("experience", ""))
        job_copy.setdefault("experience", "")
        job_copy.setdefault("posted_date", "")
        jobs_by_company[company].append(job_copy)
    
    sorted_companies = sorted(jobs_by_company.keys())
    jobs_by_company_sorted = {company: jobs_by_company[company] for company in sorted_companies}
    
    if scan_stats is None:
        scan_stats = {
            "companies_scanned": 0,
            "jobs_found": total_count or len(unique_jobs),
            "indian_jobs_matched": len(unique_jobs),
            "duplicates_removed": 0,
            "providers_failed": 0
        }
    
    return template.render(
        jobs=unique_jobs,
        jobs_by_company=dict(jobs_by_company_sorted),
        total_count=total_count or len(unique_jobs),
        current_date=datetime.now().strftime("%B %d, %Y"),
        stats=scan_stats
    )


def send_today_jobs_email() -> bool:
    from services.job_service import get_jobs_by_date
    
    if not SMTP_USER or not SMTP_PASSWORD:
        from services.logging_service import email_logger
        email_logger.error("Email credentials not configured")
        return False
    
    jobs = get_jobs_by_date(datetime.now().strftime("%Y-%m-%d"))
    
    jobs_list = [{
        "company": j.company,
        "title": j.title,
        "location": j.location,
        "url": j.url,
        "posted_date": j.posted_date,
        "employment_type": j.employment_type,
        "experience": j.experience,
        "career_page": None
    } for j in jobs]
    
    today_str = datetime.now().strftime("%d %b %Y")
    subject = f"🚀 {len(jobs_list)} New Software Jobs - {today_str}"
    
    html_content = render_job_report_template(jobs_list, len(jobs_list))
    
    return send_email(subject, html_content)