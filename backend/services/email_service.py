import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from jinja2 import Template

load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_TO = os.getenv("EMAIL_TO", "")


def send_email(subject: str, html_content: str):
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


def render_job_report_template(jobs: list) -> str:
    template = Template("""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        h1 { color: #333; text-align: center; }
        .job { border-bottom: 1px solid #eee; padding: 15px 0; }
        .job:last-child { border-bottom: none; }
        .company { font-weight: bold; color: #1a73e8; font-size: 16px; }
        .title { font-size: 14px; margin: 5px 0; color: #444; }
        .location { color: #666; font-size: 13px; }
        .apply-link { display: inline-block; margin-top: 8px; color: #1a73e8; text-decoration: none; }
        .footer { text-align: center; margin-top: 20px; color: #999; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>StartXNow Career Watch</h1>
        {% for job in jobs %}
        <div class="job">
            <div class="company">{{ job.company }}</div>
            <div class="title">{{ job.title }}</div>
            <div class="location">{{ job.location }}</div>
            <a href="{{ job.url }}" class="apply-link">Apply Now</a>
        </div>
        {% endfor %}
        <div class="footer">Generated on {{ date }}</div>
    </div>
</body>
</html>
""")
    from datetime import datetime
    return template.render(jobs=jobs, date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))