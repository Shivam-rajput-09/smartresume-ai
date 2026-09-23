"""
Unit tests for Phase 4: NLP Preprocessing & Skill Extraction Engine
"""

import pytest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.nlp_preprocessor import NLPPreprocessor, parse_resume_nlp
from src.extractor import extract_resume_text


@pytest.fixture
def nlp():
    return NLPPreprocessor()


def test_clean_text(nlp):
    raw = "John   Doe \t\t Resume\n\n\n\nSkills: Python,   Flask"
    cleaned = nlp.clean_text(raw)
    assert "John Doe Resume" in cleaned
    assert "\n\n\n" not in cleaned


def test_tokenization_and_lemmatization(nlp):
    sample = "The senior developers are building predictive models using frameworks"
    tokens = nlp.tokenize_and_lemmatize(sample)
    assert isinstance(tokens, list)
    assert "the" not in tokens  # Stopword removed
    assert "developer" in tokens or "building" in tokens or "model" in tokens or "framework" in tokens


def test_extract_contact_info(nlp):
    text = (
        "Rahul Sharma\n"
        "Email: rahul.sharma@example.com\n"
        "Phone: +91 9876543210\n"
        "LinkedIn: https://linkedin.com/in/rahulsharma\n"
        "GitHub: github.com/rahulsharma\n"
    )
    contact = nlp.extract_contact_info(text)
    assert contact["email"] == "rahul.sharma@example.com"
    assert "9876543210" in contact["phone"]
    assert "linkedin.com/in/rahulsharma" in contact["linkedin"]
    assert "github.com/rahulsharma" in contact["github"]
    assert "Rahul" in contact["name"]


def test_extract_education(nlp):
    text = "Education: Bachelor of Computer Applications (BCA) from Pune University, MCA in 2024"
    edu = nlp.extract_education(text)
    assert "BCA" in edu or "MCA" in edu


def test_extract_experience_years(nlp):
    text1 = "I have 2.5 years of experience in backend development."
    text2 = "Completed 6 months internship as QA Engineer."
    text3 = "Fresh graduate with no prior experience."
    
    assert nlp.extract_experience_years(text1) == 2.5
    assert nlp.extract_experience_years(text2) == 0.5
    assert nlp.extract_experience_years(text3) == 0.0


def test_extract_skills_single_and_multiword(nlp):
    text = "Skilled in Python, C++, Machine Learning, Deep Learning, Docker, and REST API."
    skills, categories = nlp.extract_skills(text)
    
    assert "python" in skills
    assert "c++" in skills
    assert "machine learning" in skills
    assert "deep learning" in skills
    assert "docker" in skills
    assert "rest api" in skills or "restful apis" in skills
    
    # Check categorization
    assert "Programming Languages" in categories
    assert "Data Science & Machine Learning" in categories


def test_full_nlp_parse_on_sample_resume():
    sample_file = BASE_DIR / "data" / "sample_resumes" / "sample_python_developer.txt"
    extracted = extract_resume_text(sample_file)
    parsed = parse_resume_nlp(extracted["text"])
    
    assert parsed["contact_info"]["email"] == "aarav.sharma@example.com"
    assert parsed["skills_count"] >= 8
    assert "python" in parsed["skills"]
    assert "django" in parsed["skills"]
    assert "postgresql" in parsed["skills"]
    assert parsed["experience_years"] >= 1.0
    assert len(parsed["sections_detected"]) >= 3
