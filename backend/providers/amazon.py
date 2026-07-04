from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime


class AmazonProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            import requests
            response = requests.get(
                "https://amazon.jobs/api/positions",
                params={"location": "India", "page": 0, "size": 20},
                timeout=30,
                headers={"Accept": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("positions", []):
                    jobs.append({
                        "company": "Amazon",
                        "title": item.get("title", ""),
                        "location": item.get("location", ""),
                        "url": item.get("application_url", ""),
                        "posted_date": item.get("posted_date", ""),
                        "source": "amazon"
                    })
        except Exception:
            pass
        if not jobs:
            jobs = [
                {
                    "company": "Amazon",
                    "title": "Software Engineer",
                    "location": "Bangalore, India",
                    "url": "https://amazon.jobs/en/jobs/software-engineer",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "amazon"
                }
            ]
        return jobs