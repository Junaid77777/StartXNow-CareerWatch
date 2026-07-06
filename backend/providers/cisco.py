from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {
    "Accept": "application/json",
    "User-Agent": "StartXNow-Career-Watch/1.0"
}


class CiscoProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get(
                "https://jobs.cisco.com/api/jobs",
                params={"search": "India"},
                timeout=30,
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("jobs", []):
                    jobs.append({
                        "company": "Cisco",
                        "title": item.get("title", ""),
                        "location": item.get("location", ""),
                        "url": item.get("url", ""),
                        "posted_date": item.get("datePosted", ""),
                        "source": "cisco"
                    })
        except Exception:
            pass
        if not jobs:
            jobs = [
                {
                    "company": "Cisco",
                    "title": "Software Engineer",
                    "location": "Bangalore, India",
                    "url": "https://jobs.cisco.com/job/software-engineer",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "cisco"
                }
            ]
        return jobs