"""
SmartResume AI — Skill-Gap Analysis & Learning Roadmap Engine

Compares candidate skills against target job requirements, calculates
skill-gap metrics, prioritizes missing skills, and generates an actionable,
step-by-step learning roadmap with project recommendations.
"""

from typing import Dict, List, Any, Optional, Union
from src.dataset_loader import dataset_loader


class SkillGapEngine:
    """Analyzes candidate skill deficits and generates structured learning pathways."""
    
    # Priority mapping based on technical domain depth
    SKILL_TIER_PRIORITY = {
        # Tier 1: Fundamental Programming & Core Systems (Highest)
        "python": 1, "java": 1, "c++": 1, "javascript": 1, "sql": 1,
        "data structures": 1, "algorithms": 1, "oop": 1,
        
        # Tier 2: Core Frameworks & Primary Databases
        "django": 2, "flask": 2, "fastapi": 2, "spring boot": 2,
        "react": 2, "node.js": 2, "express.js": 2, "postgresql": 2,
        "mysql": 2, "mongodb": 2, "machine learning": 2, "deep learning": 2,
        "pandas": 2, "scikit-learn": 2, "manual testing": 2, "automation testing": 2,
        
        # Tier 3: Libraries, Secondary Tools & Cloud
        "redis": 3, "docker": 3, "git": 3, "aws": 3, "rest api": 3,
        "restful apis": 3, "selenium": 3, "pytest": 3, "tableau": 3,
        "power bi": 3, "tensorflow": 3, "pytorch": 3, "linux": 3,
        
        # Tier 4: DevOps, Orchestration & Advanced Tooling (Supplementary)
        "kubernetes": 4, "ci/cd": 4, "jenkins": 4, "terraform": 4,
        "ansible": 4, "microservices": 4, "graphql": 4
    }
    
    PROJECT_SUGGESTIONS = {
        "Python Developer": {
            "title": "Scalable RESTful Microservices API",
            "desc": "Build a modular e-commerce or booking engine using Django/FastAPI, PostgreSQL, Redis caching, and Docker."
        },
        "Java Developer": {
            "title": "Enterprise Cloud Banking Service",
            "desc": "Architect a secure Spring Boot microservices backend with Spring Security, JWT, Hibernate, and MySQL."
        },
        "Data Analyst": {
            "title": "Executive Business Intelligence Dashboard",
            "desc": "Perform ETL on real-world transaction data with SQL and Pandas, and build interactive KPI charts in Power BI."
        },
        "Data Scientist": {
            "title": "End-to-End Customer Churn & Lifetime Value Predictor",
            "desc": "Train and tune Scikit-learn classification models, perform feature engineering, and deploy a Flask web demo."
        },
        "Machine Learning Engineer": {
            "title": "Multimodal Semantic Search & NLP Pipeline",
            "desc": "Fine-tune Transformer / PyTorch models for semantic document retrieval and serve predictions via FastAPI and Docker."
        },
        "Frontend Developer": {
            "title": "Responsive Single-Page Web Application",
            "desc": "Build an interactive dashboard in React with Redux Toolkit, Tailwind CSS, dark mode, and REST API integration."
        },
        "Backend Developer": {
            "title": "High-Throughput Collaborative API",
            "desc": "Design a Node.js/Express distributed API featuring WebSockets, MongoDB, Redis pub/sub, and JWT auth."
        },
        "QA Engineer": {
            "title": "Automated Web & API Regression Test Framework",
            "desc": "Develop a test automation framework using Selenium WebDriver, PyTest, Allure reporting, and GitHub Actions CI/CD."
        }
    }

    @classmethod
    def prioritize_skill(cls, skill_name: str) -> int:
        """Assigns an integer priority tier (1 = Highest / Fundamental, 4 = Advanced / Tooling)."""
        return cls.SKILL_TIER_PRIORITY.get(skill_name.lower().strip(), 3)

    @classmethod
    def analyze_gap(
        cls, candidate_skills: List[str], target_role_id_or_name: Union[int, str]
    ) -> Dict[str, Any]:
        """
        Performs in-depth skill-gap analysis comparing candidate skills
        against the target job role's mandatory and preferred requirements.
        """
        # Find target role
        if isinstance(target_role_id_or_name, int):
            job = dataset_loader.get_role_by_id(target_role_id_or_name)
        else:
            job = dataset_loader.get_role_by_name(str(target_role_id_or_name))
            
        if not job:
            raise ValueError(f"Job role '{target_role_id_or_name}' not found in dataset.")

        cand_set = {s.lower().strip() for s in candidate_skills}
        req_set = {s.lower().strip() for s in job["required_skills"]}
        pref_set = {s.lower().strip() for s in job["preferred_skills"]}

        # Mandatory Skills Breakdown
        possessed_required = sorted(list(cand_set.intersection(req_set)))
        missing_required = sorted(list(req_set - cand_set))
        
        # Preferred Skills Breakdown
        possessed_preferred = sorted(list(cand_set.intersection(pref_set)))
        missing_preferred = sorted(list(pref_set - cand_set))

        # Sort missing skills by educational prerequisite priority
        prioritized_missing_req = sorted(
            missing_required, key=lambda s: (cls.prioritize_skill(s), s)
        )
        
        # Gap Metrics
        req_count = len(req_set)
        possessed_req_count = len(possessed_required)
        match_percentage = round((possessed_req_count / req_count * 100.0), 1) if req_count else 0.0
        
        # Estimated time to bridge gap (approx 1.5 - 2 weeks per missing core skill)
        est_weeks = max(1, len(missing_required) * 2) if missing_required else 0
        
        # Readiness category
        if match_percentage >= 80:
            readiness_label = "Ready to Apply (High Fit)"
            readiness_color = "success"
        elif match_percentage >= 50:
            readiness_label = "Near Ready (Minor Skill Gap)"
            readiness_color = "warning"
        else:
            readiness_label = "Significant Upskilling Required"
            readiness_color = "danger"

        # Generate custom structured learning roadmap
        roadmap = cls.generate_roadmap(job, prioritized_missing_req, missing_preferred)

        return {
            "role_id": job["role_id"],
            "role_name": job["role_name"],
            "category": job["category"],
            "description": job["description"],
            "match_percentage": match_percentage,
            "readiness_label": readiness_label,
            "readiness_color": readiness_color,
            "total_required_skills": len(req_set),
            "possessed_required_skills": possessed_required,
            "missing_required_skills": prioritized_missing_req,
            "possessed_preferred_skills": possessed_preferred,
            "missing_preferred_skills": missing_preferred,
            "estimated_weeks_to_bridge": est_weeks,
            "roadmap": roadmap
        }

    @classmethod
    def generate_roadmap(
        cls, job: Dict[str, Any], missing_required: List[str], missing_preferred: List[str]
    ) -> Dict[str, Any]:
        """
        Builds a progressive 4-phase learning journey tailored to the candidate's specific gap.
        """
        role_name = job["role_name"]
        
        # Phase 1: Core Missing Prerequisites (High Priority)
        phase1_skills = [s for s in missing_required if cls.prioritize_skill(s) <= 2]
        # Phase 2: Missing Secondary / Framework Skills
        phase2_skills = [s for s in missing_required if cls.prioritize_skill(s) > 2]
        # Phase 3: Preferred & Tooling Enhancements
        phase3_skills = missing_preferred[:3]
        
        milestones = []
        step_num = 1
        
        if phase1_skills:
            milestones.append({
                "step": step_num,
                "title": "Phase 1: Core Fundamentals & Prerequisite Mastery",
                "focus_skills": phase1_skills,
                "goal": f"Master core concepts and foundational syntax for: {', '.join(phase1_skills)}.",
                "duration": f"{len(phase1_skills) * 2} Weeks"
            })
            step_num += 1
            
        if phase2_skills:
            milestones.append({
                "step": step_num,
                "title": "Phase 2: Frameworks, APIs & Database Integration",
                "focus_skills": phase2_skills,
                "goal": f"Build practical hands-on mini-projects utilizing: {', '.join(phase2_skills)}.",
                "duration": f"{len(phase2_skills) * 2} Weeks"
            })
            step_num += 1
            
        if phase3_skills:
            milestones.append({
                "step": step_num,
                "title": "Phase 3: Industry Tooling & Preferred Stack",
                "focus_skills": phase3_skills,
                "goal": f"Gain working familiarity with good-to-have tools: {', '.join(phase3_skills)}.",
                "duration": f"{len(phase3_skills) * 1} Weeks"
            })
            step_num += 1
            
        # Final Phase: Capstone Portfolio Project
        proj_info = cls.PROJECT_SUGGESTIONS.get(role_name, {
            "title": f"End-to-End {role_name} Showcase Project",
            "desc": f"Design and deploy a full-featured application integrating all core technologies required for {role_name}."
        })
        
        milestones.append({
            "step": step_num,
            "title": f"Phase {step_num}: Capstone Portfolio Project & Deployment",
            "project_title": proj_info["title"],
            "project_description": proj_info["desc"],
            "goal": "Build, document, and publish a production-ready repository on GitHub with live demo.",
            "duration": "2-3 Weeks"
        })

        return {
            "role_title": role_name,
            "official_learning_path": job["learning_path"],
            "milestones": milestones,
            "recommended_capstone": proj_info
        }


# Global engine instance
skill_gap_engine = SkillGapEngine()


def analyze_skill_gap(
    candidate_skills: List[str], target_role_id_or_name: Union[int, str]
) -> Dict[str, Any]:
    return skill_gap_engine.analyze_gap(candidate_skills, target_role_id_or_name)
