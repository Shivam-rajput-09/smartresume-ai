"""
SmartResume AI — Phase 7 Interactive ML Recommendation Demonstration

Demonstrates the Supervised Machine Learning Classifier predicting job roles
with calibrated confidence probabilities across classes.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.ml_recommender import predict_job_role_ml, ml_recommender

def main():
    print("=" * 75)
    print("  SmartResume AI — Phase 7 Machine Learning Recommendation Model Demo")
    print("=" * 75)
    
    test_profiles = [
        {
            "candidate": "Profile A (Full-Stack Python Dev)",
            "skills": ["python", "django", "flask", "postgresql", "rest api", "docker", "git", "javascript"]
        },
        {
            "candidate": "Profile B (AI / Deep Learning Researcher)",
            "skills": ["python", "machine learning", "deep learning", "tensorflow", "pytorch", "nlp", "pandas", "scikit-learn"]
        },
        {
            "candidate": "Profile C (QA Automation Tester)",
            "skills": ["selenium", "pytest", "automation testing", "manual testing", "postman", "jira", "sql"]
        },
        {
            "candidate": "Profile D (Frontend React Specialist)",
            "skills": ["html", "css", "javascript", "react", "typescript", "bootstrap", "tailwind css", "git"]
        }
    ]
    
    for prof in test_profiles:
        print(f"\n[+] Candidate: {prof['candidate']}")
        print(f"    Provided Skills ({len(prof['skills'])}): {', '.join(prof['skills'])}")
        
        prediction = predict_job_role_ml(prof["skills"], top_n=3)
        print(f"    -> PREDICTED PRIMARY ROLE: {prediction['predicted_role'].upper()} (Confidence: {prediction['confidence']}%)")
        print(f"    -> Algorithm Engine:       {prediction['model_used']}")
        print("    -> Top 3 Probabilities:")
        for rank, p in enumerate(prediction["top_predictions"], 1):
            bar = "#" * int(p["confidence_percentage"] / 5)
            print(f"       {rank}. {p['role_name']:<28} [{p['confidence_percentage']:>5.1f}%] {bar}")
        print("-" * 75)
        
    print("\n  Phase 7 Demonstration Complete & Verified!\n")

if __name__ == "__main__":
    main()
