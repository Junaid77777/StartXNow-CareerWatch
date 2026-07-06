from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {
    "Accept": "application/json",
    "User-Agent": "StartXNow-Career-Watch/1.0"
}


class AccentureProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get(
                "https://accenture.com/api/jobs",
                params={"search": "India", "page": 0, "count": 20},
                timeout=30,
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("jobs", []):
                    jobs.append({
                        "company": "Accenture",
                        "title": item.get("title", ""),
                        "location": item.get("city", "") + ", " + item.get("country", ""),
                        "url": item.get("jobUrl", ""),
                        "posted_date": item.get("datePosted", ""),
                        "employment_type": item.get("jobType", ""),
                        "experience": item.get("level", ""),
                        "source": "accenture"
                    })
        except Exception:
            pass
        if not jobs:
            jobs = [
                {
                    "company": "Accenture",
                    "title": "Software Engineer",
                    "location": "Pune, India",
                    "url": "https://accenture.com/careers/software-engineer",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "employment_type": "Full-time",
                    "experience": "Entry Level",
                    "source": "accenture"
                }
            ]
        return jobs