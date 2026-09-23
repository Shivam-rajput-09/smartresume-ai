"""
Unit tests for Phase 2: Job and Skill Dataset Modules
"""

import pytest
import os
import sys
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.dataset_loader import DatasetLoader
from config import Config


@pytest.fixture
def loader():
    return DatasetLoader(Config.JOB_DATASET_CSV, Config.SKILLS_DATASET_JSON)


def test_skills_json_loading(loader):
    """Verify that skills dataset loads properly and has multiple categories."""
    categories = loader.get_skill_categories()
    assert isinstance(categories, dict)
    assert len(categories) >= 5
    assert "Programming Languages" in categories
    assert "Data Science & Machine Learning" in categories


def test_skill_normalization_and_aliases(loader):
    """Verify skill normalization and alias resolution."""
    assert loader.normalize_skill("  JS  ") == "javascript"
    assert loader.normalize_skill("ReactJS") == "react"
    assert loader.normalize_skill("ML") == "machine learning"
    assert loader.normalize_skill("Sklearn") == "scikit-learn"
    assert loader.normalize_skill("python") == "python"


def test_job_roles_csv_loading(loader):
    """Verify that job roles CSV loads and contains expected roles."""
    jobs = loader.get_all_jobs()
    assert len(jobs) >= 10
    
    role_names = [j["role_name"] for j in jobs]
    assert "Python Developer" in role_names
    assert "Data Analyst" in role_names
    assert "Machine Learning Engineer" in role_names
    assert "QA Engineer" in role_names


def test_job_role_structure(loader):
    """Verify individual job role schema and skill parsing."""
    job = loader.get_role_by_name("Python Developer")
    assert job is not None
    assert job["role_id"] == 1
    assert "python" in job["required_skills"]
    assert "sql" in job["required_skills"]
    assert isinstance(job["preferred_skills"], list)
    assert len(job["learning_path"]) > 0


def test_get_role_by_id(loader):
    """Verify retrieval by ID."""
    job = loader.get_role_by_id(1)
    assert job is not None
    assert job["role_name"] == "Python Developer"
    
    non_existent = loader.get_role_by_id(9999)
    assert non_existent is None


def test_known_skills_flattened(loader):
    """Verify flattened unique skills list."""
    all_skills = loader.get_all_known_skills()
    assert isinstance(all_skills, set)
    assert "python" in all_skills
    assert "machine learning" in all_skills
    assert "selenium" in all_skills
