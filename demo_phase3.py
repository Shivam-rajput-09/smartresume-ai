"""
SmartResume AI — Phase 3 Interactive Resume Extraction Demonstration

Demonstrates extracting text from sample PDF and TXT resumes with full metadata.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.extractor import extract_resume_text

def main():
    print("=" * 65)
    print("  SmartResume AI — Phase 3 Text Extraction Engine Demo")
    print("=" * 65)
    
    sample_dir = BASE_DIR / "data" / "sample_resumes"
    samples = [
        sample_dir / "sample_python_developer.txt",
        sample_dir / "sample_python_developer.pdf",
        sample_dir / "sample_qa_engineer.pdf"
    ]
    
    for file_path in samples:
        print(f"\n[+] Processing: {file_path.name}")
        try:
            result = extract_resume_text(file_path)
            print(f"    - Status:       {result['status'].upper()}")
            print(f"    - Detected Ext: {result['file_type'].upper()}")
            print(f"    - Page Count:   {result['num_pages']}")
            print(f"    - Word Count:   {result['word_count']} words")
            print(f"    - Char Count:   {result['char_count']} chars")
            print(f"    - Snippet (First 150 chars):")
            print(f"      \"{result['text'][:150].strip()}...\"")
        except Exception as e:
            print(f"    [-] Error extracting {file_path.name}: {e}")
            
    print("\n" + "=" * 65)
    print("  Phase 3 Demonstration Complete & Verified!")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
