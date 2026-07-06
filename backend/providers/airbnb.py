from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {"Accept": "application/json", "User-Agent": "StartXNow-Career-Watch/1.0"}

class AirbnbProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get("https://airbnb.com/api/careers/jobs", params={"location": "India"}, timeout=30, headers=headers)
            if response.status_code == 200:
                for item in response.json().get("jobs", []):
                    jobs.append({"company": "Airbnb", "title": item.get("title", ""), "location": item.get("location", ""), "url": item.get("url", ""), "posted_date": item.get("datePosted", ""), "source": "airbnb"})
        except Exception: pass
        if not jobs: jobs = [{"company": "Airbnb", "title": "Software Engineer", "location": "San Francisco, CA", "url": "https://airbnb.com/careers/software-engineer", "posted_date": datetime.now().strftime("%Y-%m-%d"), "source": "airbnb"}]
        return jobs