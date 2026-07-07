import json
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional


ACCEPT_ROLES = [
    "software engineer", "software developer", "sde", "backend engineer",
    "python developer", "full stack developer", "data engineer",
    "data scientist", "ai engineer", "ml engineer", "devops engineer",
    "associate software engineer", "graduate engineer", "graduate program",
    "campus hire"
]

REJECT_ROLES = [
    "hr", "marketing", "finance", "sales", "support", "consultant",
    "manager", "lead", "principal", "architect", "director"
]

ACCEPT_EXPERIENCE = [
    "0 years", "1 year", "2 years", "fresh graduate",
    "campus", "entry level", "associate"
]

REJECT_EXPERIENCE = [
    "3+ years", "5+ years", "senior", "lead", "principal", "architect"
]

ACCEPT_LOCATIONS = [
    "bangalore", "hyderabad", "pune", "chennai", "noida", "gurugram",
    "mumbai", "delhi", "ahmedabad", "coimbatore", "kochi", "kolkata",
    "remote india", "remote (india)"
]


def load_preferences() -> Dict[str, Any]:
    with open('config.json', 'r') as f:
        config = json.load(f)
    return {
        "include_roles": config.get("filters", {}).get("roles", ACCEPT_ROLES),
        "include_locations": ACCEPT_LOCATIONS,
        "include_experience": ACCEPT_EXPERIENCE,
        "reject_experience": REJECT_EXPERIENCE,
        "country": config.get("filters", {}).get("country", "India")
    }


def job_matches_role(title: str) -> bool:
    title_lower = (title or "").lower()
    if any(reject in title_lower for reject in REJECT_ROLES):
        return False
    return any(role in title_lower for role in ACCEPT_ROLES)


def job_matches_location(location: str, preferences: Dict[str, Any]) -> bool:
    if not location:
        return False
    location_lower = (location or "").lower()
    if "india" in location_lower:
        return True
    return any(loc in location_lower for loc in preferences.get("include_locations", []))


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
    for reject in preferences.get("reject_experience", REJECT_EXPERIENCE):
        if reject in exp_lower:
            return False
    return any(exp in exp_lower for exp in preferences.get("include_experience", ACCEPT_EXPERIENCE))


def job_is_fresher(experience: str) -> bool:
    exp_lower = (experience or "").lower()
    fresher_indicators = ["entry level", "0 years", "1 year", "2 years", "fresh graduate", "campus", "associate", "intern"]
    return any(ind in exp_lower for ind in fresher_indicators)


def get_url_hash(url: str) -> str:
    return hashlib.md5(url.encode()).hexdigest()


def filter_job(job: Dict[str, Any], preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if preferences is None:
        preferences = load_preferences()
    
    title = str(job.get("title", ""))
    location = str(job.get("location", ""))
    experience = str(job.get("experience", ""))
    posted_date = job.get("posted_date")
    
    result = {
        "passed": True,
        "reject_reason": None,
        "role_ok": True,
        "location_ok": True,
        "date_ok": True,
        "experience_ok": True
    }
    
    if not job_matches_role(title):
        result["passed"] = False
        result["reject_reason"] = "role"
        result["role_ok"] = False
        return result
    
    if not job_matches_location(location, preferences):
        result["passed"] = False
        result["reject_reason"] = "location"
        result["location_ok"] = False
        return result
    
    if not job_is_recent(posted_date):
        result["passed"] = False
        result["reject_reason"] = "date"
        result["date_ok"] = False
        return result
    
    if not job_matches_experience(experience, preferences):
        result["passed"] = False
        result["reject_reason"] = "experience"
        result["experience_ok"] = False
        return result
    
    return result


def apply_filters(jobs: List[Dict[str, Any]], preferences: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    accepted = []
    rejected = []
    stats = {
        "total_jobs": len(jobs),
        "accepted_count": 0,
        "rejected_count": 0,
        "role_rejected": 0,
        "location_rejected": 0,
        "date_rejected": 0,
        "experience_rejected": 0
    }
    
    for job in jobs:
        result = filter_job(job, preferences)
        if result["passed"]:
            accepted.append(job)
            stats["accepted_count"] += 1
        else:
            rejected.append({"job": job, "reason": result["reject_reason"]})
            stats["rejected_count"] += 1
            if result["reject_reason"] == "role":
                stats["role_rejected"] += 1
            elif result["reject_reason"] == "location":
                stats["location_rejected"] += 1
            elif result["reject_reason"] == "date":
                stats["date_rejected"] += 1
            elif result["reject_reason"] == "experience":
                stats["experience_rejected"] += 1
    
    return {
        "accepted": accepted,
        "rejected": rejected,
        "stats": stats
    }


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