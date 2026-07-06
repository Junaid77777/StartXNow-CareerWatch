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
        from services.logging_service import email_logger
        email_logger.error(f"Failed to send email: {str(e)}")
        return False


def is_remote(job: dict) -> bool:
    location = str(job.get("location", "")).lower()
    return "remote" in location


def is_hybrid(job: dict) -> bool:
    employment_type = str(job.get("employment_type", "")).lower()
    return "hybrid" in employment_type


def render_job_report_template(jobs: list, total_count: int = 0) -> str:
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
        .summary {
            padding: 20px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
            text-align: center;
        }
        .summary .count {
            font-size: 36px;
            font-weight: 700;
            color: #1a73e8;
        }
        .summary .label {
            color: #666;
            font-size: 14px;
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
            margin-bottom: 6px;
        }
        .job-location {
            color: #6c757d;
            font-size: 14px;
            margin-bottom: 8px;
        }
        .job-badges {
            margin-bottom: 12px;
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
        .job-meta {
            font-size: 13px;
            color: #868e96;
            margin-bottom: 12px;
        }
        .apply-btn {
            display: inline-block;
            background: #1a73e8;
            color: white !important;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 500;
            transition: background 0.2s;
        }
        .apply-btn:hover { background: #0d47a1; }
        .career-link {
            display: inline-block;
            margin-left: 12px;
            color: #6c757d;
            font-size: 13px;
            text-decoration: none;
        }
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
            <h1>StartXNow AI Daily Career Report</h1>
            <div class="date">{{ current_date }}</div>
        </div>
        
        <div class="summary">
            <div class="count">{{ total_count }}</div>
            <div class="label">new matching jobs found</div>
        </div>
        
        {% if jobs %}
            {% for company, company_jobs in jobs_by_company.items() %}
            <div class="company-group">
                <div class="company-name">{{ company }} ({{ company_jobs|length }} position{{ 's' if company_jobs|length > 1 else '' }})</div>
                {% for job in company_jobs %}
                <div class="job">
                    <div class="job-title">{{ job.title }}</div>
                    <div class="job-location">{{ job.location }}</div>
                    
                    <div class="job-badges">
                        {% if job.is_remote %}<span class="badge badge-remote">Remote</span>{% endif %}
                        {% if job.is_hybrid %}<span class="badge badge-hybrid">Hybrid</span>{% endif %}
                        {% if job.is_entry_level %}<span class="badge badge-entry">Entry Level</span>{% endif %}
                    </div>
                    
                    <div class="job-meta">
                        {% if job.posted_date %}Posted: {{ job.posted_date }}{% endif %}
                        {% if job.employment_type %}<span class="separator">•</span> {{ job.employment_type }}{% endif %}
                    </div>
                    
                    <a href="{{ job.url }}" class="apply-btn">Direct Apply</a>
                    {% if job.career_page %}<a href="{{ job.career_page }}" class="career-link">Career Page</a>{% endif %}
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
    
    jobs_by_company = defaultdict(list)
    for job in jobs:
        company = job.get("company", "Unknown")
        job_copy = dict(job)
        job_copy["is_remote"] = is_remote(job)
        job_copy["is_hybrid"] = is_hybrid(job)
        job_copy["is_entry_level"] = job_is_fresher(job.get("experience", ""))
        jobs_by_company[company].append(job_copy)
    
    return template.render(
        jobs=jobs,
        jobs_by_company=dict(jobs_by_company),
        total_count=total_count or len(jobs),
        current_date=datetime.now().strftime("%B %d, %Y")
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
        "career_page": f"https://{(j.company or '').lower()}.com/careers" if j.company else None
    } for j in jobs]
    
    html_content = render_job_report_template(jobs_list, len(jobs))
    
    return send_email("StartXNow AI Daily Career Report", html_content)