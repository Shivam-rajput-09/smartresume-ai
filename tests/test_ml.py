"""
Unit tests for Phase 7: Machine Learning Recommendation Engine
"""

import pytest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.ml_recommender import MLRecommender, predict_job_role_ml


@pytest.fixture
def ml_engine():
    return MLRecommender()


def test_synthetic_data_generation(ml_engine):
    X, y = ml_engine.generate_synthetic_training_data(samples_per_role=10)
    assert len(X) == len(y)
    assert len(X) >= 100
    assert "Python Developer" in y
    assert "QA Engineer" in y
    assert "Data Scientist" in y


def test_model_training_and_metrics(ml_engine):
    metrics = ml_engine.train_and_compare_models()
    assert "champion_model" in metrics
    assert "models_comparison" in metrics
    assert len(metrics["models_comparison"]) == 5
    assert "KNN (K-Nearest Neighbors)" in metrics["models_comparison"]
    assert "Logistic Regression" in metrics["models_comparison"]


def test_saved_model_artifacts(ml_engine):
    assert ml_engine.model_path.exists()
    assert ml_engine.vectorizer_path.exists()
    assert ml_engine.metrics_path.exists()


def test_predict_python_developer(ml_engine):
    skills = ["python", "django", "flask", "postgresql", "rest api", "git", "docker"]
    pred = ml_engine.predict(skills, top_n=3)
    
    assert pred["predicted_role"] in ["Python Developer", "Backend Developer"]
    assert pred["confidence"] > 40.0
    assert len(pred["top_predictions"]) == 3
    assert pred["top_predictions"][0]["role_name"] == pred["predicted_role"]


def test_predict_data_scientist(ml_engine):
    skills = ["python", "machine learning", "deep learning", "tensorflow", "scikit-learn", "pandas", "nlp"]
    pred = ml_engine.predict(skills, top_n=3)
    
    assert pred["predicted_role"] in ["Data Scientist", "Machine Learning Engineer"]
    assert pred["confidence"] > 40.0


def test_predict_empty_skills(ml_engine):
    pred = ml_engine.predict([])
    assert "predicted_role" in pred
    assert pred["confidence"] == 0.0
