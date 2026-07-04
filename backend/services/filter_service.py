import json
from typing import List, Dict, Any
import re


def filter_job(job: Dict[str, Any], filters: Dict[str, Any] = None) -> bool:
    if filters is None:
        filters = load_filters()
    
    title = str(job.get("title", "")).lower()
    location = str(job.get("location", "")).lower()
    
    role_keywords = [str(r).lower() for r in filters.get("roles", [])]
    location_keywords = [str(l).lower() for l in filters.get("locations", [])]
    
    title_match = any(kw in title for kw in role_keywords)
    
    location_match = any(kw in location for kw in location_keywords)
    
    return title_match or location_match


def load_filters():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config.get("filters", {
        "roles": [],
        "locations": [],
        "experience": []
    })


def apply_filters(jobs: List[Dict[str, Any]], filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    filtered = []
    for job in jobs:
        if filter_job(job, filters):
            filtered.append(job)
    return filtered