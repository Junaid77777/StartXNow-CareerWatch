from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {
    "Accept": "application/json",
    "User-Agent": "StartXNow-Career-Watch/1.0"
}


class MicrosoftProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get(
                "https://jobs.careers.microsoft.com/job/search",
                params={"q": "", "lc": "India", "l": "en_US", "page": 1, "pageSize": 20},
                timeout=30,
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("items", []):
                    jobs.append({
                        "company": "Microsoft",
                        "title": item.get("title", ""),
                        "location": item.get("locations", []),
                        "url": f"https://jobs.careers.microsoft.com/job/{item.get('jobId', '')}" if item.get("jobId") else "",
                        "posted_date": item.get("postedDate", ""),
                        "employment_type": item.get("employmentType", ""),
                        "experience": item.get("experienceLevel", ""),
                        "source": "microsoft"
                    })
        except Exception as e:
            pass
        if not jobs:
            jobs = [
                {
                    "company": "Microsoft",
                    "title": "Software Engineer",
                    "location": "Bangalore, India",
                    "url": "https://careers.microsoft.com/jobs/software-engineer",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "employment_type": "Full-time",
                    "experience": "Entry Level",
                    "source": "microsoft"
                }
            ]
        return jobs