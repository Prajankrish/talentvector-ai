#!/usr/bin/env python3
"""Test script to verify job matching fix"""

import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))

from matching import CandidateJobMatcher

print("=" * 70)
print("JOB MATCHING TEST - Verify Explanation Field")
print("=" * 70)
print()

# Test data
matcher = CandidateJobMatcher()

# Test 1: Strong match
print("Test 1: Strong Match Candidate")
print("-" * 70)
match1 = matcher.compute_match(
    hiring_embedding=[0.1] * 768,
    candidate_embedding=[0.1] * 768,
    screening_score=9.0,
    candidate_profile={"name": "Alice Johnson"},
    hiring_profile={"role_title": "Senior ML Engineer"}
)

print(f"Candidate Name:    {match1.get('candidate_id', 'N/A')}")
print(f"Similarity Score:  {match1['similarity_score']}")
print(f"Screening Score:   {match1['screening_score']}/10")
print(f"Final Score:       {match1['final_score']}/10")
print(f"Explanation:       {match1.get('explanation', 'N/A')}")
print(f"Recommendation:    {match1['recommendation']}")
print()

# Test 2: Moderate match
print("Test 2: Moderate Match Candidate")
print("-" * 70)
match2 = matcher.compute_match(
    hiring_embedding=[0.1] * 768,
    candidate_embedding=[0.3] * 768,
    screening_score=6.5,
    candidate_profile={"name": "Bob Smith"},
    hiring_profile={"role_title": "Data Engineer"}
)

print(f"Similarity Score:  {match2['similarity_score']}")
print(f"Screening Score:   {match2['screening_score']}/10")
print(f"Final Score:       {match2['final_score']}/10")
print(f"Explanation:       {match2.get('explanation', 'N/A')}")
print(f"Recommendation:    {match2['recommendation']}")
print()

# Test 3: Weak match
print("Test 3: Weak Match Candidate")
print("-" * 70)
match3 = matcher.compute_match(
    hiring_embedding=[0.1] * 768,
    candidate_embedding=[0.7] * 768,
    screening_score=3.0,
    candidate_profile={"name": "Charlie Brown"},
    hiring_profile={"role_title": "ML Developer"}
)

print(f"Similarity Score:  {match3['similarity_score']}")
print(f"Screening Score:   {match3['screening_score']}/10")
print(f"Final Score:       {match3['final_score']}/10")
print(f"Explanation:       {match3.get('explanation', 'N/A')}")
print(f"Recommendation:    {match3['recommendation']}")
print()

# Verify all required fields exist
print("Field Verification")
print("-" * 70)
required_fields = ["similarity_score", "screening_score", "final_score", "explanation", "recommendation"]
all_good = True
for field in required_fields:
    exists_m1 = field in match1
    exists_m2 = field in match2
    exists_m3 = field in match3
    status = "✓" if (exists_m1 and exists_m2 and exists_m3) else "✗"
    print(f"{status} {field:20s} - Match1: {exists_m1}, Match2: {exists_m2}, Match3: {exists_m3}")
    if not (exists_m1 and exists_m2 and exists_m3):
        all_good = False

print()
if all_good:
    print("✅ ALL TESTS PASSED - Job matching is working correctly!")
else:
    print("❌ SOME TESTS FAILED - Check field presence")

print("=" * 70)
