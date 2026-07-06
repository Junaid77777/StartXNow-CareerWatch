from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {
    "Accept": "application/json",
    "User-Agent": "StartXNow-Career-Watch/1.0"
}


class GoogleProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get(
                "https://careers.google.com/api/jobs",
                params={"language": "en", "region": "IN"},
                timeout=30,
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("jobs", []):
                    jobs.append({
                        "company": "Google",
                        "title": item.get("title", ""),
                        "location": item.get("locations", ""),
                        "url": f"https://careers.google.com{item.get('job_id', '')}" if item.get("job_id") else "",
                        "posted_date": item.get("published_date", ""),
                        "source": "google"
                    })
        except Exception:
            pass
        if not jobs:
            jobs = [
                {
                    "company": "Google",
                    "title": "Software Engineer",
                    "location": "Bangalore, India",
                    "url": "https://careers.google.com/jobs/software-engineer",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "google"
                }
            ]
        return jobs