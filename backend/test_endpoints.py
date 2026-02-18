#!/usr/bin/env python3
"""Test both Resume and Hiring Profile endpoints"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("="*60)
print("TESTING API ENDPOINTS")
print("="*60)

# Test 1: Resume Parsing
print("\n[TEST 1] Resume Parsing Endpoint")
print("-" * 60)

resume_data = {
    "resume_text": "John Doe software engineer 10 years Python JavaScript Google Apple CS degree"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/parse-resume",
        json=resume_data,
        timeout=30
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {list(data.keys())}")
        print(f"Success: True")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")

# Test 2: Hiring Profile
print("\n[TEST 2] Hiring Profile Endpoint")
print("-" * 60)

hiring_data = {
    "role_title": "Senior Software Engineer",
    "required_skills": ["Python", "JavaScript", "Docker"],
    "nice_to_have_skills": ["Go", "Kubernetes"],
    "years_of_experience": 10,
    "industry": "Technology",
    "team_culture_description": "Collaborative, agile team with focus on innovation",
    "job_level": "Senior",
    "salary_range": "$150k-$200k",
    "qualifications": "BS in Computer Science or equivalent"
}

try:
    response = requests.post(
        f"{BASE_URL}/api/hiring-profile",
        json=hiring_data,
        timeout=30
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response keys: {list(data.keys())}")
        print(f"Success: True")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)
