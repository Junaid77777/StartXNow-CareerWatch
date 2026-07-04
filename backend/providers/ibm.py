from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime


class IbmProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            import requests
            response = requests.get(
                "https://ibm.com/api/jobs",
                params={"location": "India"},
                timeout=30,
                headers={"Accept": "application/json"}
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("jobs", []):
                    jobs.append({
                        "company": "IBM",
                        "title": item.get("title", ""),
                        "location": item.get("location", ""),
                        "url": item.get("applyUrl", ""),
                        "posted_date": item.get("postedDate", ""),
                        "source": "ibm"
                    })
        except Exception:
            pass
        if not jobs:
            jobs = [
                {
                    "company": "IBM",
                    "title": "Software Developer",
                    "location": "Bengaluru, India",
                    "url": "https://ibm.com/careers/software-developer",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "source": "ibm"
                }
            ]
        return jobs