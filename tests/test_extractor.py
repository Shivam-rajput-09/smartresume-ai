"""
Unit tests for Phase 3: Resume Text Extraction Engine
"""

import pytest
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.extractor import ResumeExtractor, ResumeExtractorError, extract_resume_text


@pytest.fixture
def sample_dir():
    return BASE_DIR / "data" / "sample_resumes"


def test_extract_txt_valid(sample_dir):
    """Verify text extraction from a valid TXT resume."""
    txt_path = sample_dir / "sample_python_developer.txt"
    assert txt_path.exists()
    
    result = extract_resume_text(txt_path)
    assert result["status"] == "success"
    assert result["file_type"] == "txt"
    assert "AARAV SHARMA" in result["text"]
    assert "Python" in result["text"]
    assert "Django" in result["text"]
    assert result["word_count"] > 100
    assert result["num_pages"] == 1


def test_extract_pdf_valid(sample_dir):
    """Verify text extraction from a valid PDF resume."""
    pdf_path = sample_dir / "sample_python_developer.pdf"
    assert pdf_path.exists()
    
    result = extract_resume_text(pdf_path)
    assert result["status"] == "success"
    assert result["file_type"] == "pdf"
    assert "PYTHON DEVELOPER" in result["text"]
    assert "Flask" in result["text"]
    assert result["word_count"] > 30
    assert result["num_pages"] >= 1


def test_is_allowed_file():
    """Verify file extension validator."""
    assert ResumeExtractor.is_allowed_file("resume.pdf") is True
    assert ResumeExtractor.is_allowed_file("my_cv.txt") is True
    assert ResumeExtractor.is_allowed_file("profile.DOCX") is True
    assert ResumeExtractor.is_allowed_file("script.py") is False
    assert ResumeExtractor.is_allowed_file("photo.jpg") is False
    assert ResumeExtractor.is_allowed_file("malicious.exe") is False
    assert ResumeExtractor.is_allowed_file("") is False


def test_extract_non_existent_file():
    """Verify exception when file does not exist."""
    with pytest.raises(FileNotFoundError):
        extract_resume_text("C:/non_existent_path/fake_resume.pdf")


def test_extract_empty_file(tmp_path):
    """Verify error handling on an empty (0-byte) resume file."""
    empty_file = tmp_path / "empty_resume.txt"
    empty_file.write_text("", encoding="utf-8")
    
    with pytest.raises(ResumeExtractorError):
        extract_resume_text(empty_file)


def test_unsupported_format(tmp_path):
    """Verify error handling on an unsupported file format."""
    bad_file = tmp_path / "resume.exe"
    bad_file.write_text("dummy binary payload", encoding="utf-8")
    
    with pytest.raises(ResumeExtractorError):
        extract_resume_text(bad_file)
