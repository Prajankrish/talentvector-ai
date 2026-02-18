#!/usr/bin/env python3
"""Test Pydantic models to identify validation issues"""

import json
from main import ResumeParsingRequest, HiringProfileRequest

# Test 1: Resume Parsing Request
print("=" * 60)
print("TEST 1: ResumeParsingRequest")
print("=" * 60)

test_resume_data = {
    "resume_text": "John Doe is a software engineer with 5 years of experience in Python and JavaScript"
}

try:
    request = ResumeParsingRequest(**test_resume_data)
    print("✅ ResumeParsingRequest validation PASSED")
    print(f"Request data: {request.model_dump()}")
except Exception as e:
    print(f"❌ ResumeParsingRequest validation FAILED: {e}")
    print(f"Test data: {json.dumps(test_resume_data, indent=2)}")

# Test 2: Hiring Profile Request  
print("\n" + "=" * 60)
print("TEST 2: HiringProfileRequest")
print("=" * 60)

test_hiring_data = {
    "role_title": "Software Engineer",
    "required_skills": ["Python", "JavaScript"],
    "nice_to_have_skills": ["Go", "Rust"],
    "years_of_experience": 3,
    "industry": "Technology",
    "team_culture_description": "Agile and collaborative",
    "job_level": "Senior",
    "salary_range": "$120k-$150k",
    "qualifications": "BS in Computer Science"
}

try:
    request = HiringProfileRequest(**test_hiring_data)
    print("✅ HiringProfileRequest validation PASSED")
    print(f"Request data: {request.model_dump()}")
except Exception as e:
    print(f"❌ HiringProfileRequest validation FAILED: {e}")
    print(f"Test data: {json.dumps(test_hiring_data, indent=2)}")

# Test 3: Hiring Profile Request with minimal data
print("\n" +"=" * 60)
print("TEST 3: HiringProfileRequest (minimal fields)")
print("=" * 60)

test_hiring_minimal = {
    "role_title": "Software Engineer",
    "required_skills": ["Python"],
    "years_of_experience": 3,
    "industry": "Tech",
    "team_culture_description": "Agile"
}

try:
    request = HiringProfileRequest(**test_hiring_minimal)
    print("✅ HiringProfileRequest (minimal) validation PASSED")
    print(f"Request data: {request.model_dump()}")
except Exception as e:
    print(f"❌ HiringProfileRequest (minimal) validation FAILED: {e}")
    print(f"Test data: {json.dumps(test_hiring_minimal, indent=2)}")
