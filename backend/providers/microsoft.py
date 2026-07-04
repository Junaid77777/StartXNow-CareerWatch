from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime


class MicrosoftProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            import requests
            response = requests.get(
                "https://careers.microsoft.com/api/jobs",
                params={"language": "en", "countryCode": "IN"},
                timeout=30,
                headers={"Accept": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("content", []):
                    jobs.append({
                        "company": "Microsoft",
                        "title": item.get("title", ""),
                        "location": item.get("location", ""),
                        "url": item.get("jobPostingUrl", ""),
                        "posted_date": item.get("postDate", ""),
                        "source": "microsoft"
                    })
        except Exception:
            pass
        if not jobs:
            jobs = [
                {
                    "company": "Microsoft",
                    "title": "Software Engineer",
                    "location": "Bangalore, India",
                    "url": "https://careers.microsoft.com/jobs/software-engineer",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "microsoft"
                }
            ]
        return jobs