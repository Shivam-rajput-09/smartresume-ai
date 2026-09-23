"""
SmartResume AI — Phase 1 Environment & Setup Verification Script

This script verifies that all required dependencies are installed,
downloads necessary NLTK datasets, and ensures project directories exist.
"""

import sys
import os
from pathlib import Path

def print_header(title):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)

def check_python_version():
    print(f"[*] Python Version: {sys.version.split()[0]} ({sys.executable})")
    if sys.version_info < (3, 9):
        print("[!] Warning: Python 3.9+ is recommended.")
    else:
        print("[+] Python version check: OK")

def check_dependencies():
    print_header("Checking Required Packages")
    packages = [
        ("flask", "Flask Web Framework"),
        ("pandas", "Pandas Data Analysis"),
        ("numpy", "NumPy Numerical Computing"),
        ("sklearn", "Scikit-learn Machine Learning"),
        ("nltk", "NLTK Natural Language Processing"),
        ("matplotlib", "Matplotlib Data Visualization"),
        ("PyPDF2", "PyPDF2 PDF Parser"),
        ("pdfplumber", "pdfplumber PDF Parser"),
        ("selenium", "Selenium Browser Automation"),
        ("pytest", "Pytest Testing Framework"),
        ("sqlite3", "SQLite Database Support")
    ]
    
    all_ok = True
    for module_name, desc in packages:
        try:
            import importlib.metadata
            mod = __import__(module_name)
            try:
                ver = importlib.metadata.version(module_name)
            except Exception:
                ver = getattr(mod, '__version__', 'built-in')
            print(f"  [+] {desc:35} (v{ver}) ... OK")
        except ImportError as e:
            print(f"  [-] {desc:35} ... MISSING ({e})")
            all_ok = False
            
    return all_ok

def setup_nltk():
    print_header("Downloading NLTK Corpora & Tokenizers")
    try:
        import nltk
        resources = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger', 'punkt_tab']
        for res in resources:
            try:
                nltk.download(res, quiet=True)
                print(f"  [+] NLTK Resource '{res}' ... Downloaded/Ready")
            except Exception as e:
                print(f"  [!] NLTK Resource '{res}' download issue: {e}")
    except ImportError:
        print("  [-] NLTK is not installed yet.")

def create_directory_structure():
    print_header("Creating & Verifying Project Directories")
    base_dir = Path(__file__).resolve().parent
    directories = [
        base_dir / "app" / "static" / "css",
        base_dir / "app" / "static" / "js",
        base_dir / "app" / "templates",
        base_dir / "data" / "sample_resumes",
        base_dir / "src",
        base_dir / "tests",
        base_dir / "uploads",
        base_dir / "docs"
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        rel_path = directory.relative_to(base_dir)
        print(f"  [+] Directory ready: {rel_path}")

def init_package_files():
    base_dir = Path(__file__).resolve().parent
    init_files = [
        base_dir / "src" / "__init__.py",
        base_dir / "app" / "__init__.py",
        base_dir / "tests" / "__init__.py"
    ]
    for init_file in init_files:
        if not init_file.exists():
            init_file.write_text("# Package initializer\n", encoding="utf-8")

if __name__ == "__main__":
    print_header("SmartResume AI — Environment Verification")
    check_python_version()
    create_directory_structure()
    init_package_files()
    deps_ok = check_dependencies()
    if deps_ok:
        setup_nltk()
        print_header("Phase 1 Setup Verification Complete!")
        print("  SUCCESS: SmartResume AI environment and folder structure are fully configured.")
        print("  Ready to proceed to Phase 2: Job & Skill Dataset Creation.\n")
    else:
        print_header("Phase 1 Setup Incomplete")
        print("  Please install missing dependencies using:")
        print("  pip install -r requirements.txt\n")
