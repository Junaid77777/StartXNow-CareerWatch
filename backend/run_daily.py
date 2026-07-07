import asyncio

from database import init_db
from services.scheduler_service import collect_daily_jobs
from services.email_service import send_today_jobs_email

async def main():
    print("Initializing database...")
    init_db()

    print("Collecting jobs...")
    result = await collect_daily_jobs()
    print(result)

    print("Sending email...")
    success = send_today_jobs_email()

    if success:
        print("✅ Email sent successfully")
    else:
        print("❌ Failed to send email")
        raise Exception("Email sending failed")

if __name__ == "__main__":
    asyncio.run(main())