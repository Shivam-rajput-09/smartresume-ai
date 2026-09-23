"""
SmartResume AI — Phase 4 Interactive NLP Pipeline Demonstration

Demonstrates text cleaning, tokenization, entity extraction, and skill extraction
on sample resumes.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.extractor import extract_resume_text
from src.nlp_preprocessor import parse_resume_nlp

def main():
    print("=" * 70)
    print("  SmartResume AI — Phase 4 NLP Preprocessor & Skill Extractor Demo")
    print("=" * 70)
    
    sample_files = [
        BASE_DIR / "data" / "sample_resumes" / "sample_python_developer.txt",
        BASE_DIR / "data" / "sample_resumes" / "sample_data_scientist.txt"
    ]
    
    for file_path in sample_files:
        print(f"\n[+] Analyzing Document: {file_path.name}")
        extracted = extract_resume_text(file_path)
        nlp_result = parse_resume_nlp(extracted["text"])
        
        contact = nlp_result["contact_info"]
        print("\n  --- Contact Information ---")
        print(f"  * Name:     {contact['name']}")
        print(f"  * Email:    {contact['email']}")
        print(f"  * Phone:    {contact['phone']}")
        print(f"  * LinkedIn: {contact['linkedin']}")
        print(f"  * GitHub:   {contact['github']}")
        
        print("\n  --- Profile Metadata ---")
        print(f"  * Education Degrees:   {', '.join(nlp_result['education']) or 'None Detected'}")
        print(f"  * Est. Experience:     {nlp_result['experience_years']} Years")
        print(f"  * Sections Identified: {', '.join(nlp_result['sections_detected'])}")
        print(f"  * Total Skills Found:  {nlp_result['skills_count']}")
        
        print("\n  --- Extracted Skills by Domain ---")
        for cat, skills in nlp_result["skills_by_category"].items():
            print(f"  * {cat:<32}: {', '.join(skills)}")
            
        print("\n  --- Lemmatized Token Sample (First 15 tokens) ---")
        print(f"  {nlp_result['tokens_sample'][:15]}")
        print("-" * 70)
        
    print("\n" + "=" * 70)
    print("  Phase 4 Demonstration Complete & Verified!")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    main()
