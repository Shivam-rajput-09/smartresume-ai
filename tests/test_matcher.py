"""
Unit tests for Phase 6: Baseline Job Matching Engine
"""

import pytest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.matcher import JobMatcher, match_jobs_baseline
from src.extractor import extract_resume_text
from src.nlp_preprocessor import parse_resume_nlp


@pytest.fixture
def matcher():
    return JobMatcher()


def test_prepare_job_corpus(matcher):
    assert len(matcher.job_corpus) >= 10
    assert matcher.job_tfidf_matrix is not None
    assert matcher.job_tfidf_matrix.shape[0] == len(matcher.jobs)


def test_calculate_skill_overlap(matcher):
    candidate_skills = ["python", "django", "sql", "git"]
    required_skills = ["python", "django", "flask", "sql", "git", "rest api"]
    
    overlap = matcher.calculate_skill_overlap(candidate_skills, required_skills)
    assert "python" in overlap["matched_skills"]
    assert "django" in overlap["matched_skills"]
    assert "flask" in overlap["missing_skills"]
    assert "rest api" in overlap["missing_skills"]
    assert overlap["matched_count"] == 4
    assert overlap["required_count"] == 6
    assert 60 <= overlap["overlap_percentage"] <= 70


def test_match_python_developer_resume(matcher):
    sample_file = BASE_DIR / "data" / "sample_resumes" / "sample_python_developer.txt"
    extracted = extract_resume_text(sample_file)
    parsed = parse_resume_nlp(extracted["text"])
    
    recommendations = matcher.match_resume(
        parsed["skills"], extracted["text"], top_n=5
    )
    
    assert len(recommendations) == 5
    # Rank 1 should be Python Developer or Backend Developer
    top_role = recommendations[0]["role_name"]
    assert top_role in ["Python Developer", "Backend Developer", "Software Developer"]
    assert recommendations[0]["match_percentage"] >= 65.0
    assert recommendations[0]["rank"] == 1
    
    # Check monotonic descending order
    for i in range(len(recommendations) - 1):
        assert recommendations[i]["match_percentage"] >= recommendations[i+1]["match_percentage"]


def test_match_qa_engineer_resume(matcher):
    sample_file = BASE_DIR / "data" / "sample_resumes" / "sample_qa_engineer.pdf"
    extracted = extract_resume_text(sample_file)
    parsed = parse_resume_nlp(extracted["text"])
    
    recommendations = matcher.match_resume(
        parsed["skills"], extracted["text"], top_n=5
    )
    assert len(recommendations) == 5
    role_names = [r["role_name"] for r in recommendations]
    assert "QA Engineer" in role_names[:2]


def test_match_specific_role(matcher):
    candidate_skills = ["python", "django", "flask", "sql", "git"]
    match = matcher.match_specific_role("Python Developer", candidate_skills)
    assert match is not None
    assert match["role_name"] == "Python Developer"
    assert match["match_percentage"] > 50.0
