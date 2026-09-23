"""
SmartResume AI — Phase 9 Interactive Flask & REST API Backend Demo

Demonstrates backend initialization, SQLite database transactions,
and direct REST API calls for headless resume text analysis.
"""

import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from app import create_app
from app.models import Database
from config import Config

def main():
    print("=" * 75)
    print("  SmartResume AI — Phase 9 Flask Backend & SQLite Database Demo")
    print("=" * 75)
    
    app = create_app(Config)
    client = app.test_client()
    
    # 1. Test REST API Endpoint (/api/analyze-text)
    sample_text = (
        "Rohit Verma\n"
        "Email: rohit.verma@example.com | Phone: +91 9988776655\n"
        "Summary: Python Developer with strong background in Flask, Django, SQL, and REST APIs.\n"
        "Skills: Python, Django, Flask, FastAPI, PostgreSQL, Docker, Git, Pytest, Linux\n"
        "Education: Bachelor of Computer Applications (BCA AI)\n"
        "Experience: 1.5 years of experience in backend development\n"
        "Projects: Built an inventory management microservice and automated data pipelines."
    )
    
    print("\n[+] Testing Headless REST API: POST /api/analyze-text")
    response = client.post(
        '/api/analyze-text',
        data=json.dumps({"text": sample_text}),
        content_type='application/json'
    )
    
    if response.status_code == 200:
        data = response.get_json()
        print(f"    * Response Status:   HTTP {response.status_code} OK")
        print(f"    * Extracted Skills:  {', '.join(data['parsed_nlp']['skills'])}")
        print(f"    * Resume Score:      {data['score_data']['total_score']}/100 (Grade: {data['score_data']['grade']})")
        print(f"    * ML Predicted Role: {data['ml_prediction']['predicted_role']} ({data['ml_prediction']['confidence']}%)")
        print("    * Top 3 Recommendations:")
        for r in data['recommendations'][:3]:
            print(f"      - {r['role_name']:<25} (Match: {r['match_percentage']}%)")
    else:
        print(f"    [-] API Request failed with code {response.status_code}")
        
    # 2. Test SQLite Database CRUD
    print("\n[+] Inspecting SQLite Database Scan Records:")
    all_scans = Database.get_all_scans(limit=5)
    print(f"    * Total Scan Records Stored: {len(all_scans)}")
    for s in all_scans[:3]:
        print(f"      - [ID: {s['id']}] {s['candidate_name']:<20} | Score: {s['resume_score']} | ML Role: {s['ml_predicted_role']}")
        
    print("\n" + "=" * 75)
    print("  Phase 9 Demonstration Complete & Verified!")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    main()
