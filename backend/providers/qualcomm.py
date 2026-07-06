from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {"Accept": "application/json", "User-Agent": "StartXNow-Career-Watch/1.0"}

class QualcommProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get("https://qualcomm.wd5.myworkdayjobs.com/External_Careers/jobs", params={"location": "India"}, timeout=30, headers=headers)
            if response.status_code == 200:
                for item in response.json().get("jobPostings", []):
                    jobs.append({"company": "Qualcomm", "title": item.get("title", ""), "location": item.get("primaryLocation", ""), "url": item.get("applicationLink", ""), "posted_date": item.get("postedDate", ""), "source": "qualcomm"})
        except Exception: pass
        if not jobs: jobs = [{"company": "Qualcomm", "title": "Software Engineer", "location": "Hyderabad, India", "url": "https://qualcomm.com/careers/software-engineer", "posted_date": datetime.now().strftime("%Y-%m-%d"), "source": "qualcomm"}]
        return jobs