"""
SmartResume AI — Phase 6 Interactive Job Recommendation Demo

Demonstrates TF-IDF Vectorization, Cosine Similarity, and Skill Overlap
recommending Top-5 job roles for candidate resumes.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.extractor import extract_resume_text
from src.nlp_preprocessor import parse_resume_nlp
from src.matcher import match_jobs_baseline

def main():
    print("=" * 75)
    print("  SmartResume AI — Phase 6 Baseline Job Recommendation Demo (TF-IDF & Overlap)")
    print("=" * 75)
    
    samples = [
        BASE_DIR / "data" / "sample_resumes" / "sample_python_developer.txt",
        BASE_DIR / "data" / "sample_resumes" / "sample_data_scientist.txt",
        BASE_DIR / "data" / "sample_resumes" / "sample_qa_engineer.pdf"
    ]
    
    for sample_path in samples:
        print(f"\n[+] Analyzing Recommendations For: {sample_path.name}")
        extracted = extract_resume_text(sample_path)
        parsed = parse_resume_nlp(extracted["text"])
        
        recs = match_jobs_baseline(parsed["skills"], extracted["text"], top_n=5)
        
        print(f"  Extracted Skills ({len(parsed['skills'])}): {', '.join(parsed['skills'][:10])}...")
        print("\n  --- Top 5 Recommended Job Roles ---")
        print(f"  {'Rank':<5} {'Role Name':<28} {'Match %':<10} {'Skill Overlap':<15} {'TF-IDF Sim':<12}")
        print("  " + "-" * 70)
        
        for r in recs:
            print(
                f"  #{r['rank']:<4} {r['role_name']:<28} "
                f"{r['match_percentage']:>5.1f}%     "
                f"{r['skill_overlap_percentage']:>5.1f}%         "
                f"{r['tfidf_similarity_percentage']:>5.1f}%"
            )
            
        # Top 1 Role Detailed Skill Breakdown
        top_1 = recs[0]
        print(f"\n  [* Top Match Analysis: {top_1['role_name']}]")
        print(f"  * Matched Skills ({len(top_1['matched_skills'])}): {', '.join(top_1['matched_skills'])}")
        print(f"  * Missing Skills ({len(top_1['missing_skills'])}): {', '.join(top_1['missing_skills']) if top_1['missing_skills'] else 'None (100% Match!)'}")
        print("=" * 75)
        
    print("\n  Phase 6 Demonstration Complete & Verified!\n")

if __name__ == "__main__":
    main()
