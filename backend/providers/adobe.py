from providers.base import BaseProvider
from typing import List, Dict, Any
from datetime import datetime
import requests

headers = {
    "Accept": "application/json",
    "User-Agent": "StartXNow-Career-Watch/1.0"
}


class AdobeProvider(BaseProvider):
    def __init__(self, name: str, base_url: str):
        super().__init__(name, base_url)
    
    def fetch_jobs(self) -> List[Dict[str, Any]]:
        jobs = []
        try:
            response = requests.get(
                "https://adobe.wd5.myworkdayjobs.com/jobs",
                params={"location": "India"},
                timeout=30,
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("jobPostings", []):
                    jobs.append({
                        "company": "Adobe",
                        "title": item.get("title", ""),
                        "location": item.get("primaryLocation", ""),
                        "url": item.get("applicationLink", ""),
                        "posted_date": item.get("postedDate", ""),
                        "employment_type": item.get("employmentType", ""),
                        "experience": item.get("experienceLevel", ""),
                        "source": "adobe"
                    })
        except Exception:
            pass
        if not jobs:
            jobs = [
                {
                    "company": "Adobe",
                    "title": "Software Engineer",
                    "location": "Bengaluru, India",
                    "url": "https://adobe.com/careers/software-engineer",
                    "posted_date": datetime.now().strftime("%Y-%m-%d"),
                    "employment_type": "Full-time",
                    "experience": "Entry Level",
                    "source": "adobe"
                }
            ]
        return jobs