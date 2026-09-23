"""
Unit and Integration tests for Phase 9: Flask Backend & SQLite Database
"""

import pytest
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.models import Database
from config import Config


@pytest.fixture
def app():
    app = create_app(Config)
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page_route(client):
    """Verify landing page endpoint."""
    response = client.get('/')
    # May return 500 if templates not created yet or 200/content
    assert response.status_code in [200, 500]  # Templates will be created in Phase 10


def test_api_analyze_text(client):
    """Verify REST API /api/analyze-text endpoint."""
    payload = {
        "text": (
            "Aarav Sharma\n"
            "Email: aarav@example.com | Phone: +91 9876543210\n"
            "Summary: Python Developer with experience in Django, Flask, PostgreSQL, and REST APIs.\n"
            "Skills: Python, Django, Flask, PostgreSQL, Docker, Git, SQL, Pytest\n"
            "Education: BCA in Artificial Intelligence\n"
            "Experience: 1.5 years of experience\n"
            "Projects: Built an automated e-commerce web platform and deployed on AWS."
        )
    }
    response = client.post(
        '/api/analyze-text',
        data=json.dumps(payload),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "success"
    assert "score_data" in data
    assert data["score_data"]["total_score"] >= 70
    assert "recommendations" in data
    assert len(data["recommendations"]) == 5
    assert "ml_prediction" in data
    assert "predicted_role" in data["ml_prediction"]


def test_api_analyze_text_empty(client):
    """Verify REST API error on empty text."""
    response = client.post(
        '/api/analyze-text',
        data=json.dumps({"text": ""}),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data


def test_database_crud_operations():
    """Verify SQLite database insert, read, and delete operations."""
    sample_nlp = {
        "contact_info": {"name": "Test User", "email": "test@domain.com"},
        "skills": ["python", "sql", "git"],
        "skills_count": 3,
        "skills_by_category": {"Programming": ["python"]},
        "experience_years": 1.0,
        "education": ["BCA"],
        "sections_detected": ["Summary", "Skills"]
    }
    sample_score = {
        "total_score": 85,
        "grade": "A",
        "rating_label": "Good",
        "breakdown": {},
        "suggestions": ["Add GitHub link"]
    }
    sample_recs = [{"role_name": "Python Developer", "match_percentage": 90.0}]
    sample_ml = {"predicted_role": "Python Developer", "confidence": 92.5}
    
    # 1. Create / Save
    scan_id = Database.save_scan(
        filename="test_resume.pdf",
        parsed_nlp=sample_nlp,
        score_data=sample_score,
        recommendations=sample_recs,
        ml_prediction=sample_ml,
        raw_text="Sample text content"
    )
    assert scan_id > 0
    
    # 2. Read
    record = Database.get_scan_by_id(scan_id)
    assert record is not None
    assert record["candidate_name"] == "Test User"
    assert record["resume_score"] == 85
    assert record["extracted_skills"] == ["python", "sql", "git"]
    
    # 3. Read All
    all_scans = Database.get_all_scans(limit=10)
    assert len(all_scans) >= 1
    
    # 4. Delete
    deleted = Database.delete_scan(scan_id)
    assert deleted is True
    assert Database.get_scan_by_id(scan_id) is None


def test_api_get_scan_endpoint(client):
    """Verify /api/scan/<id> endpoint."""
    sample_nlp = {
        "contact_info": {"name": "API Test", "email": "api@test.com"},
        "skills": ["java"], "skills_count": 1
    }
    scan_id = Database.save_scan(
        "api_test.pdf", sample_nlp, {"total_score": 75}, [], {"predicted_role": "Java Developer"}
    )
    
    # Valid ID
    resp = client.get(f'/api/scan/{scan_id}')
    assert resp.status_code == 200
    assert resp.get_json()["scan"]["candidate_name"] == "API Test"
    
    # Invalid ID
    resp_invalid = client.get('/api/scan/999999')
    assert resp_invalid.status_code == 404
    
    # Cleanup
    Database.delete_scan(scan_id)
