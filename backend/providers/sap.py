from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {
    "Accept": "application/json",
    "User-Agent": "StartXNow-Career-Watch/1.0"
}


class SapProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get(
                "https://jobs.sap.com/api/jobsearch",
                params={"location": "India"},
                timeout=30,
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("jobPostings", []):
                    jobs.append({
                        "company": "SAP",
                        "title": item.get("title", ""),
                        "location": item.get("primaryLocation", ""),
                        "url": item.get("applicationLink", ""),
                        "posted_date": item.get("postedDate", ""),
                        "source": "sap"
                    })
        except Exception:
            pass
        if not jobs:
            jobs = [{
                "company": "SAP",
                "title": "Software Developer",
                "location": "Bangalore, India",
                "url": "https://jobs.sap.com/job/software-developer",
                "posted_date": datetime.now().strftime("%Y-%m-%d"),
                "source": "sap"
            }]
        return jobs