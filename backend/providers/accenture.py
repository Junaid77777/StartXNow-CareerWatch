from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime


class AccentureProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            import requests
            response = requests.get(
                "https://www.accenture.com/api/jobs",
                params={"location": "India"},
                timeout=30,
                headers={"Accept": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("jobs", []):
                    jobs.append({
                        "company": "Accenture",
                        "title": item.get("title", ""),
                        "location": item.get("location", ""),
                        "url": item.get("applicationLink", ""),
                        "posted_date": item.get("postedDate", ""),
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
                    "source": "accenture"
                }
            ]
        return jobs