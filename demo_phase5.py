"""
SmartResume AI — Phase 5 Interactive Resume Scoring Demonstration

Demonstrates the 100-point transparent scoring system with multi-factor breakdown
and personalized recommendations.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.extractor import extract_resume_text
from src.nlp_preprocessor import parse_resume_nlp
from src.scorer import score_resume_nlp

def main():
    print("=" * 70)
    print("  SmartResume AI — Phase 5 Resume Scoring Engine Demo")
    print("=" * 70)
    
    samples = [
        BASE_DIR / "data" / "sample_resumes" / "sample_python_developer.txt",
        BASE_DIR / "data" / "sample_resumes" / "sample_qa_engineer.pdf"
    ]
    
    for sample_path in samples:
        print(f"\n[+] Evaluating: {sample_path.name}")
        extracted = extract_resume_text(sample_path)
        parsed = parse_resume_nlp(extracted["text"])
        score_res = score_resume_nlp(parsed, extracted["text"])
        
        print("\n  ================================================================")
        print(f"  OVERALL RESUME SCORE: {score_res['total_score']} / {score_res['max_score']}  |  GRADE: {score_res['grade']}")
        print(f"  RATING: {score_res['rating_label']}")
        print("  ================================================================")
        
        b = score_res["breakdown"]
        print("\n  --- Multi-Factor Breakdown ---")
        print(f"  1. Skills & Diversity:   {b['skills']['score']:2d}/30 pts -> {b['skills']['remarks']}")
        print(f"  2. Education Level:      {b['education']['score']:2d}/20 pts -> {b['education']['remarks']}")
        print(f"  3. Work Experience:      {b['experience']['score']:2d}/20 pts -> {b['experience']['remarks']}")
        print(f"  4. Projects & Depth:     {b['projects']['score']:2d}/15 pts -> {b['projects']['remarks']}")
        print(f"  5. Completeness & Links: {b['completeness']['score']:2d}/15 pts -> {b['completeness']['remarks']}")
        
        print("\n  --- Actionable Improvement Suggestions ---")
        for i, s in enumerate(score_res["suggestions"], 1):
            print(f"   [{i}] {s}")
        print("-" * 70)
        
    print("\n" + "=" * 70)
    print("  Phase 5 Demonstration Complete & Verified!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
