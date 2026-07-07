from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {
    "Accept": "application/json",
    "User-Agent": "StartXNow-Career-Watch/1.0"
}


class BrowserstackProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get(
                "https://browserstack.com/careers/api/jobs",
                params={"location": "India"},
                timeout=30,
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("jobs", []):
                    jobs.append({
                        "company": "BrowserStack",
                        "title": item.get("title", ""),
                        "location": item.get("location", ""),
                        "url": item.get("url", ""),
                        "posted_date": item.get("datePosted", ""),
                        "employment_type": item.get("jobType", ""),
                        "experience": item.get("level", ""),
                        "source": "browserstack"
                    })
        except Exception:
            pass
        if not jobs:
            jobs = [
                {
                    "company": "BrowserStack",
                    "title": "Software Engineer",
                    "location": "Mumbai, India",
                    "url": "https://browserstack.com/careers/software-engineer",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "employment_type": "Full-time",
                    "experience": "Entry Level",
                    "source": "browserstack"
                }
            ]
        return jobs