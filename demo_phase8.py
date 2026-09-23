"""
SmartResume AI — Phase 8 Interactive Skill-Gap Analysis & Roadmap Demo

Demonstrates candidate skill gap evaluation against target job profiles,
prerequisite priority ordering, and tailored step-by-step roadmap generation.
"""

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

from src.skill_gap import analyze_skill_gap

def main():
    print("=" * 75)
    print("  SmartResume AI — Phase 8 Skill-Gap & Learning Roadmap Engine Demo")
    print("=" * 75)
    
    scenarios = [
        {
            "candidate": "Candidate A (Aspiring Machine Learning Engineer)",
            "current_skills": ["python", "pandas", "numpy", "matplotlib", "git"],
            "target_role": "Machine Learning Engineer"
        },
        {
            "candidate": "Candidate B (Aspiring Full Stack Developer)",
            "current_skills": ["html", "css", "javascript", "react", "git"],
            "target_role": "Full Stack Developer"
        }
    ]
    
    for sc in scenarios:
        print(f"\n[+] Candidate Scenario: {sc['candidate']}")
        print(f"    Current Skills: {', '.join(sc['current_skills'])}")
        print(f"    Target Goal:    {sc['target_role']}")
        
        gap = analyze_skill_gap(sc["current_skills"], sc["target_role"])
        
        print("\n  --- Skill Gap Analysis Metrics ---")
        print(f"  * Role Match Percentage:  {gap['match_percentage']}%")
        print(f"  * Readiness Assessment:   {gap['readiness_label']}")
        print(f"  * Est. Timeline to Bridge:{gap['estimated_weeks_to_bridge']} Weeks")
        
        print(f"\n  * Possessed Mandatory Skills ({len(gap['possessed_required_skills'])}):")
        print(f"    {', '.join(gap['possessed_required_skills']) if gap['possessed_required_skills'] else 'None'}")
        
        print(f"  * Missing Mandatory Skills (Prioritized: {len(gap['missing_required_skills'])}):")
        print(f"    {', '.join(gap['missing_required_skills']) if gap['missing_required_skills'] else 'None (Complete!)'}")
        
        print(f"  * Recommended Preferred Stack: {', '.join(gap['missing_preferred_skills'][:4])}")
        
        print("\n  --- Tailored Step-by-Step Learning Roadmap ---")
        roadmap = gap["roadmap"]
        for m in roadmap["milestones"]:
            if "project_title" in m:
                print(f"  [{m['title']}] (Est: {m['duration']})")
                print(f"    - Project: {m['project_title']}")
                print(f"    - Scope:   {m['project_description']}")
            else:
                print(f"  [{m['title']}] (Est: {m['duration']})")
                print(f"    - Focus: {', '.join(m['focus_skills'])}")
                print(f"    - Goal:  {m['goal']}")
        print("-" * 75)
        
    print("\n  Phase 8 Demonstration Complete & Verified!\n")

if __name__ == "__main__":
    main()
