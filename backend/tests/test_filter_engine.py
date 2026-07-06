import pytest
from services.filter_engine import (
    job_matches_role, job_matches_location, job_is_recent,
    job_matches_experience, job_is_fresher, get_url_hash, is_duplicate,
    filter_job, apply_filters, get_job_age_days, ACCEPT_ROLES, REJECT_ROLES
)


class TestRoleFiltering:
    def test_software_engineer_accepted(self):
        assert job_matches_role("Software Engineer") == True
    
    def test_software_developer_accepted(self):
        assert job_matches_role("Software Developer") == True
    
    def test_python_developer_accepted(self):
        assert job_matches_role("Python Developer") == True
    
    def test_backend_engineer_accepted(self):
        assert job_matches_role("Backend Engineer") == True
    
    def test_ai_engineer_accepted(self):
        assert job_matches_role("AI Engineer") == True
    
    def test_sde_accepted(self):
        assert job_matches_role("SDE 1") == True
    
    def test_sales_rejected(self):
        assert job_matches_role("Sales Associate") == False
    
    def test_marketing_rejected(self):
        assert job_matches_role("Marketing Manager") == False
    
    def test_hr_rejected(self):
        assert job_matches_role("HR Manager") == False
    
    def test_finance_rejected(self):
        assert job_matches_role("Finance Analyst") == False
    
    def test_recruiter_rejected(self):
        assert job_matches_role("Recruiter") == False
    
    def test_customer_support_rejected(self):
        assert job_matches_role("Customer Support Representative") == False
    
    def test_hr_role_rejected(self):
        assert job_matches_role("Software HR Specialist") == False


class TestLocationFiltering:
    def test_india_accepted(self):
        prefs = {"include_locations": ["India", "Bangalore"]}
        assert job_matches_location("Bangalore, India", prefs) == True
    
    def test_remote_accepted(self):
        prefs = {"include_locations": ["Remote"]}
        assert job_matches_location("Remote", prefs) == True
    
    def test_other_location_rejected(self):
        prefs = {"include_locations": ["India"]}
        assert job_matches_location("New York, USA", prefs) == False


class TestDateFiltering:
    def test_recent_job_accepted(self):
        today = "2026-07-06"
        assert job_is_recent(today) == True
    
    def test_old_job_rejected(self):
        old_date = "2026-06-01"
        assert job_is_recent(old_date) == False
    
    def test_none_date_accepted(self):
        assert job_is_recent(None) == True


class TestExperienceFiltering:
    def test_entry_level_accepted(self):
        prefs = {"include_experience": ["Entry Level", "Fresher"]}
        assert job_matches_experience("Entry Level", prefs) == True
    
    def test_fresher_accepted(self):
        prefs = {"include_experience": ["Fresher"]}
        assert job_matches_experience("Fresher", prefs) == True
    
    def test_senior_rejected(self):
        prefs = {"include_experience": ["Entry Level"]}
        assert job_matches_experience("Senior", prefs) == False


class TestFresherDetection:
    def test_fresher_detected(self):
        assert job_is_fresher("Entry Level") == True
    
    def test_intern_detected(self):
        assert job_is_fresher("Intern") == True


class TestUrlHash:
    def test_hash_generated(self):
        hash1 = get_url_hash("https://example.com/job/1")
        hash2 = get_url_hash("https://example.com/job/1")
        assert hash1 == hash2
    
    def test_different_hash(self):
        hash1 = get_url_hash("https://example.com/job/1")
        hash2 = get_url_hash("https://example.com/job/2")
        assert hash1 != hash2


class TestDuplicateDetection:
    def test_duplicate_detected(self):
        seen = {get_url_hash("https://example.com/job/1")}
        assert is_duplicate("https://example.com/job/1", seen) == True
    
    def test_not_duplicate(self):
        seen = set()
        assert is_duplicate("https://example.com/job/1", seen) == False


class TestJobAge:
    def test_job_age_calculated(self):
        assert get_job_age_days("2026-07-01") == 5


class TestFilterJob:
    def test_valid_job_passes(self):
        job = {"title": "Software Engineer", "location": "Bangalore, India", "experience": "Entry Level"}
        assert filter_job(job) == True
    
    def test_invalid_role_fails(self):
        job = {"title": "Sales Executive", "location": "Bangalore, India"}
        assert filter_job(job) == False
    
    def test_old_job_fails(self):
        job = {"title": "Software Engineer", "location": "Bangalore, India", "posted_date": "2026-05-01"}
        assert filter_job(job) == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])