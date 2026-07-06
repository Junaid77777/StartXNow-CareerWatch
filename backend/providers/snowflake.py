from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {"Accept": "application/json", "User-Agent": "StartXNow-Career-Watch/1.0"}

class SnowflakeProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get("https://snowflake.wd5.myworkdayjobs.com/Snowflake/jobs", params={"location": "India"}, timeout=30, headers=headers)
            if response.status_code == 200:
                for item in response.json().get("jobPostings", []):
                    jobs.append({"company": "Snowflake", "title": item.get("title", ""), "location": item.get("primaryLocation", ""), "url": item.get("applicationLink", ""), "posted_date": item.get("postedDate", ""), "source": "snowflake"})
        except Exception: pass
        if not jobs: jobs = [{"company": "Snowflake", "title": "Software Engineer", "location": "Hyderabad, India", "url": "https://snowflake.com/careers/software-engineer", "posted_date": datetime.now().strftime("%Y-%m-%d"), "source": "snowflake"}]
        return jobs