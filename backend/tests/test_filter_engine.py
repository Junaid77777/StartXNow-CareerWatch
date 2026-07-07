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
    
    def test_sde_accepted(self):
        assert job_matches_role("SDE 1") == True
    
    def test_backend_engineer_accepted(self):
        assert job_matches_role("Backend Engineer") == True
    
    def test_data_scientist_accepted(self):
        assert job_matches_role("Data Scientist") == True
    
    def test_devops_accepted(self):
        assert job_matches_role("DevOps Engineer") == True
    
    def test_sales_rejected(self):
        assert job_matches_role("Sales Associate") == False
    
    def test_marketing_rejected(self):
        assert job_matches_role("Marketing Manager") == False
    
    def test_finance_rejected(self):
        assert job_matches_role("Finance Analyst") == False
    
    def test_support_rejected(self):
        assert job_matches_role("Customer Support") == False
    
    def test_consultant_rejected(self):
        assert job_matches_role("Consultant") == False
    
    def test_manager_rejected(self):
        assert job_matches_role("Engineering Manager") == False
    
    def test_lead_rejected(self):
        assert job_matches_role("Team Lead") == False
    
    def test_architect_rejected(self):
        assert job_matches_role("Software Architect") == False
    
    def test_director_rejected(self):
        assert job_matches_role("Engineering Director") == False


class TestLocationFiltering:
    def test_india_accepted(self):
        prefs = {"include_locations": ["bangalore", "hyderabad", "pune", "chennai", "noida", "gurugram", "mumbai", "delhi", "ahmedabad", "coimbatore", "kochi", "kolkata", "remote india", "remote (india)"]}
        assert job_matches_location("Bangalore, India", prefs) == True
    
    def test_remote_india_accepted(self):
        prefs = {"include_locations": ["bangalore", "hyderabad", "pune", "chennai", "noida", "gurugram", "mumbai", "delhi", "ahmedabad", "coimbatore", "kochi", "kolkata", "remote india", "remote (india)"]}
        assert job_matches_location("Remote India", prefs) == True
    
    def test_other_location_rejected(self):
        prefs = {"include_locations": ["bangalore", "hyderabad", "pune", "chennai", "noida", "gurugram", "mumbai", "delhi", "ahmedabad", "coimbatore", "kochi", "kolkata", "remote india", "remote (india)"]}
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
        prefs = {"include_experience": ["entry level", "fresh graduate"], "reject_experience": ["senior", "lead"]}
        assert job_matches_experience("Entry Level", prefs) == True
    
    def test_associate_accepted(self):
        prefs = {"include_experience": ["associate", "entry level"], "reject_experience": ["senior", "lead"]}
        assert job_matches_experience("Associate", prefs) == True
    
    def test_senior_rejected(self):
        prefs = {"include_experience": ["entry level"], "reject_experience": ["senior", "lead"]}
        assert job_matches_experience("Senior", prefs) == False
    
    def test_3plus_years_rejected(self):
        prefs = {"include_experience": ["entry level", "associate"], "reject_experience": ["3+ years", "senior", "lead"]}
        assert job_matches_experience("3+ Years", prefs) == False


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
        from datetime import datetime, timedelta
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        assert get_job_age_days(yesterday) == 1


class TestFilterJob:
    def test_valid_job_passes(self):
        job = {"title": "Software Engineer", "location": "Bangalore, India", "experience": "Entry Level"}
        result = filter_job(job)
        assert result["passed"] == True
    
    def test_invalid_role_fails(self):
        job = {"title": "Sales Executive", "location": "Bangalore, India"}
        result = filter_job(job)
        assert result["passed"] == False
        assert result["reject_reason"] == "role"
    
    def test_old_job_fails(self):
        job = {"title": "Software Engineer", "location": "Bangalore, India", "posted_date": "2026-05-01"}
        result = filter_job(job)
        assert result["passed"] == False
        assert result["reject_reason"] == "date"


class TestApplyFilters:
    def test_returns_detailed_stats(self):
        jobs = [
            {"title": "Software Engineer", "location": "Bangalore, India", "experience": "Entry Level"},
            {"title": "Sales Executive", "location": "Bangalore, India", "experience": "Entry Level"},
            {"title": "Software Engineer", "location": "Seattle, USA", "experience": "Entry Level"},
            {"title": "Software Engineer", "location": "Bangalore, India", "experience": "5+ Years"}
        ]
        result = apply_filters(jobs)
        assert result["stats"]["total_jobs"] == 4
        assert result["stats"]["accepted_count"] == 1
        assert result["stats"]["rejected_count"] == 3
        assert result["stats"]["role_rejected"] == 1
        assert result["stats"]["location_rejected"] == 1
        assert result["stats"]["experience_rejected"] == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])