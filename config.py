import os
from pathlib import Path

# Base Directory of the Project
BASE_DIR = Path(__file__).resolve().parent

# Application Configuration
class Config:
    BASE_DIR = BASE_DIR
    SECRET_KEY = os.environ.get('SECRET_KEY', 'smartresume-ai-dev-secret-key-2026')
    
    # Directory paths
    DATA_DIR = BASE_DIR / 'data'
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    DOCS_DIR = BASE_DIR / 'docs'
    SRC_DIR = BASE_DIR / 'src'
    
    # Allowed file extensions for resume upload
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload limit
    
    # Database configuration (SQLite for portability and simplicity)
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{BASE_DIR / 'smartresume.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # ML & Dataset file paths
    JOB_DATASET_CSV = DATA_DIR / 'job_roles.csv'
    SKILLS_DATASET_JSON = DATA_DIR / 'skills_dataset.json'
    ML_MODEL_PATH = DATA_DIR / 'job_classifier_model.pkl'
    TFIDF_VECTORIZER_PATH = DATA_DIR / 'tfidf_vectorizer.pkl'
    
    # Recommendation Configuration
    TOP_N_RECOMMENDATIONS = 5
