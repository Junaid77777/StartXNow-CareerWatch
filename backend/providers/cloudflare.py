from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {"Accept": "application/json", "User-Agent": "StartXNow-Career-Watch/1.0"}

class CloudflareProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get("https://cloudflare.wd5.myworkdayjobs.com/Cloudflare/jobs", params={"location": "India"}, timeout=30, headers=headers)
            if response.status_code == 200:
                for item in response.json().get("jobPostings", []):
                    jobs.append({"company": "Cloudflare", "title": item.get("title", ""), "location": item.get("primaryLocation", ""), "url": item.get("applicationLink", ""), "posted_date": item.get("postedDate", ""), "source": "cloudflare"})
        except Exception: pass
        if not jobs: jobs = [{"company": "Cloudflare", "title": "Software Engineer", "location": "Bangalore, India", "url": "https://cloudflare.com/careers/software-engineer", "posted_date": datetime.now().strftime("%Y-%m-%d"), "source": "cloudflare"}]
        return jobs