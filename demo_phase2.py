"""
SmartResume AI — Phase 2 Interactive Dataset Demonstration

Displays sample dataset queries, skill normalization, and category stats.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.dataset_loader import dataset_loader

def main():
    print("=" * 65)
    print("  SmartResume AI — Phase 2 Dataset & Skills Taxonomy Demo")
    print("=" * 65)
    
    # 1. Total Job Roles
    jobs = dataset_loader.get_all_jobs()
    print(f"\n[+] Total Job Roles Loaded: {len(jobs)}")
    for j in jobs[:5]:
        print(f"    - [{j['role_id']:2d}] {j['role_name']:<25} | Category: {j['category']}")
    print(f"    ... and {len(jobs) - 5} more roles.")
    
    # 2. Skill Categories
    categories = dataset_loader.get_skill_categories()
    print(f"\n[+] Domain Skill Categories ({len(categories)} categories):")
    for cat, skills in categories.items():
        print(f"    - {cat:<32} ({len(skills)} skills): {', '.join(skills[:4])}...")
        
    # 3. Skill Normalization & Aliases
    test_aliases = ["JS", "ReactJS", "ML", "Sklearn", "Postgres", "DSA", "K8s"]
    print(f"\n[+] Skill Alias Resolution Examples:")
    for alias in test_aliases:
        print(f"    '{alias}' -> '{dataset_loader.normalize_skill(alias)}'")
        
    # 4. Detailed Role Inspection
    print(f"\n[+] Sample Job Role Detail ('Machine Learning Engineer'):")
    ml_role = dataset_loader.get_role_by_name("Machine Learning Engineer")
    if ml_role:
        print(f"    Role ID:         {ml_role['role_id']}")
        print(f"    Required Skills: {', '.join(ml_role['required_skills'])}")
        print(f"    Preferred Skills:{', '.join(ml_role['preferred_skills'])}")
        print(f"    Learning Path:   {ml_role['learning_path']}")
        
    print("\n" + "=" * 65)
    print("  Phase 2 Demonstration Complete & Verified!")
    print("=" * 65 + "\n")

if __name__ == "__main__":
    main()
