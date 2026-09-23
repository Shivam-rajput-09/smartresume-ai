"""
Unit tests for Phase 5: Resume Scoring Engine
"""

import pytest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.scorer import ResumeScorer, score_resume_nlp
from src.extractor import extract_resume_text
from src.nlp_preprocessor import parse_resume_nlp


def test_skills_scoring():
    # 12+ skills across 3+ domains
    high_skills = ["python", "django", "flask", "sql", "postgresql", "docker", "aws", "git", "pytest", "c++", "jwt", "linux"]
    categories = {"Programming": ["python"], "Web": ["django"], "Cloud": ["docker"]}
    res_high = ResumeScorer.calculate_skills_score(high_skills, categories)
    assert res_high["score"] == 30
    
    # 3 skills
    low_skills = ["python", "sql", "git"]
    res_low = ResumeScorer.calculate_skills_score(low_skills, {"Programming": ["python"]})
    assert res_low["score"] == 10


def test_education_scoring():
    assert ResumeScorer.calculate_education_score(["MCA"])["score"] == 20
    assert ResumeScorer.calculate_education_score(["BCA"])["score"] == 18
    assert ResumeScorer.calculate_education_score(["B.Tech"])["score"] == 18
    assert ResumeScorer.calculate_education_score(["Diploma in CS"])["score"] == 14
    assert ResumeScorer.calculate_education_score([])["score"] == 0


def test_experience_scoring():
    assert ResumeScorer.calculate_experience_score(3.5)["score"] == 20
    assert ResumeScorer.calculate_experience_score(1.5)["score"] == 15
    assert ResumeScorer.calculate_experience_score(0.5)["score"] == 12
    assert ResumeScorer.calculate_experience_score(0.0)["score"] == 8


def test_projects_scoring():
    text = "Projects: Built an automated pipeline, developed REST API, designed database and deployed on cloud."
    res = ResumeScorer.calculate_projects_score(text, ["Projects", "Skills"])
    assert res["score"] >= 12
    assert res["has_projects_section"] is True
    assert res["action_verbs_count"] >= 3


def test_completeness_scoring():
    contact = {
        "email": "test@example.com",
        "phone": "+91 9876543210",
        "linkedin": "linkedin.com/in/test",
        "github": "github.com/test"
    }
    sections = ["Summary", "Education", "Experience", "Projects", "Skills"]
    res = ResumeScorer.calculate_completeness_score(contact, sections)
    assert res["score"] == 15


def test_end_to_end_scoring_on_sample_resume():
    sample_file = BASE_DIR / "data" / "sample_resumes" / "sample_python_developer.txt"
    extracted = extract_resume_text(sample_file)
    parsed = parse_resume_nlp(extracted["text"])
    score_data = score_resume_nlp(parsed, extracted["text"])
    
    assert 0 <= score_data["total_score"] <= 100
    assert score_data["total_score"] >= 80  # Good resume with projects, experience, skills
    assert score_data["grade"] in ["A+", "A"]
    assert "breakdown" in score_data
    assert len(score_data["suggestions"]) > 0
