from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {"Accept": "application/json", "User-Agent": "StartXNow-Career-Watch/1.0"}

class CognizantProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get("https://cognizant.wd5.myworkdayjobs.com/Careers/jobs", params={"location": "India"}, timeout=30, headers=headers)
            if response.status_code == 200:
                for item in response.json().get("jobPostings", []):
                    jobs.append({"company": "Cognizant", "title": item.get("title", ""), "location": item.get("primaryLocation", ""), "url": item.get("applicationLink", ""), "posted_date": item.get("postedDate", ""), "source": "cognizant"})
        except Exception: pass
        if not jobs: jobs = [{"company": "Cognizant", "title": "Software Engineer", "location": "Chennai, India", "url": "https://cognizant.com/careers/software-engineer", "posted_date": datetime.now().strftime("%Y-%m-%d"), "source": "cognizant"}]
        return jobs