import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


ACCEPT_ROLES = [
    "software engineer", "software developer", "python developer", "backend engineer",
    "ai engineer", "machine learning engineer", "data engineer", "graduate engineer",
    "associate software engineer", "sde", "developer", "full stack", "backend"
]

REJECT_ROLES = [
    "sales", "marketing", "finance", "hr", "recruiter", "customer support",
    "operations", "legal", "accountant", "business development", "consultant"
]


def load_preferences() -> Dict[str, Any]:
    with open('config.json', 'r') as f:
        config = json.load(f)
    return {
        "include_roles": config.get("filters", {}).get("roles", ACCEPT_ROLES),
        "include_locations": config.get("filters", {}).get("locations", ["India", "Hyderabad", "Bangalore", "Remote"]),
        "include_experience": config.get("filters", {}).get("experience", ["0-2 Years", "Fresher", "Entry Level"]),
        "country": config.get("filters", {}).get("country", "India")
    }


def job_matches_role(title: str) -> bool:
    title_lower = (title or "").lower()
    if any(reject in title_lower for reject in REJECT_ROLES):
        return False
    return any(role in title_lower for role in ACCEPT_ROLES)


def job_matches_location(location: str, preferences: Dict[str, Any]) -> bool:
    if not location:
        return True
    location_lower = (location or "").lower()
    return any(loc.lower() in location_lower for loc in preferences.get("include_locations", []))


def job_is_recent(posted_date: Optional[str], include_internships: bool = True) -> bool:
    if not posted_date:
        return True
    
    try:
        date_str = posted_date.split("T")[0] if "T" in posted_date else posted_date
        if len(date_str) > 10:
            date_str = date_str[:10]
        job_date = datetime.strptime(date_str, "%Y-%m-%d")
        today = datetime.now()
        max_age = timedelta(days=30) if include_internships else timedelta(days=7)
        return (today - job_date) <= max_age
    except (ValueError, TypeError):
        return True


def job_matches_experience(experience: str, preferences: Dict[str, Any]) -> bool:
    if not experience:
        return True
    exp_lower = (experience or "").lower()
    return any(exp.lower() in exp_lower for exp in preferences.get("include_experience", []))


def job_is_fresher(experience: str) -> bool:
    exp_lower = (experience or "").lower()
    fresher_indicators = ["entry level", "0-2 years", "fresher", "intern"]
    return any(ind in exp_lower for ind in fresher_indicators)


def get_url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def filter_job(job: Dict[str, Any], preferences: Optional[Dict[str, Any]] = None) -> bool:
    if preferences is None:
        preferences = load_preferences()
    
    title = str(job.get("title", ""))
    location = str(job.get("location", ""))
    experience = str(job.get("experience", ""))
    posted_date = job.get("posted_date")
    
    if not job_matches_role(title):
        return False
    
    if not job_matches_location(location, preferences):
        return False
    
    if not job_is_recent(posted_date):
        return False
    
    if not job_matches_experience(experience, preferences):
        return False
    
    return True


def apply_filters(jobs: List[Dict[str, Any]], preferences: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    return [job for job in jobs if filter_job(job, preferences)]


def get_job_age_days(posted_date: str) -> int:
    if not posted_date:
        return 0
    try:
        date_str = posted_date.split("T")[0] if "T" in posted_date else posted_date
        if len(date_str) > 10:
            date_str = date_str[:10]
        job_date = datetime.strptime(date_str, "%Y-%m-%d")
        return (datetime.now() - job_date).days
    except (ValueError, TypeError):
        return 0


def is_duplicate(url: str, seen_urls: set) -> bool:
    return get_url_hash(url) in seen_urls