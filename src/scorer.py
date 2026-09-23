"""
SmartResume AI — Transparent Multi-Factor Resume Scoring Engine

Calculates an explainable 100-point resume quality score across 5 objective pillars:
1. Technical Skills & Diversity (30 pts)
2. Educational Qualifications (20 pts)
3. Professional & Internship Experience (20 pts)
4. Projects & Action Verbs (15 pts)
5. Resume Completeness & Professional Links (15 pts)
"""

import re
from typing import Dict, List, Any


class ResumeScorer:
    """Computes a transparent, explainable resume score with actionable feedback."""
    
    ACTION_VERBS = [
        'developed', 'built', 'implemented', 'designed', 'created', 'deployed',
        'optimized', 'engineered', 'automated', 'integrated', 'architected',
        'managed', 'trained', 'evaluated', 'analyzed', 'configured', 'tested'
    ]
    
    @classmethod
    def calculate_skills_score(cls, skills: List[str], categories: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Pillar 1: Skills & Diversity (Max: 30 pts)
        Evaluates the count of verified technical skills and domain diversity.
        """
        count = len(skills)
        num_categories = len(categories)
        
        if count >= 12 and num_categories >= 3:
            score = 30
            remarks = "Excellent technical skill set spanning multiple domains."
        elif count >= 8:
            score = 25
            remarks = "Strong skill foundation with good domain coverage."
        elif count >= 5:
            score = 18
            remarks = "Moderate skill count. Consider adding more specialized tools/frameworks."
        elif count >= 2:
            score = 10
            remarks = "Limited skills identified. Add relevant programming languages, libraries, or tools."
        else:
            score = 4
            remarks = "Critical: Very few technical skills detected."
            
        return {
            "score": score,
            "max_score": 30,
            "skills_count": count,
            "domains_count": num_categories,
            "remarks": remarks
        }

    @classmethod
    def calculate_education_score(cls, education: List[str]) -> Dict[str, Any]:
        """
        Pillar 2: Educational Qualifications (Max: 20 pts)
        Evaluates recognized academic degrees and technical credentials.
        """
        edu_str = " ".join(education).lower()
        
        if any(d in edu_str for d in ['mca', 'm.tech', 'mtech', 'm.sc', 'msc', 'phd', 'ph.d', 'master']):
            score = 20
            degree_level = "Postgraduate / Master's Degree"
        elif any(d in edu_str for d in ['bca', 'b.tech', 'btech', 'b.e.', 'be', 'b.sc', 'bsc', 'bachelor']):
            score = 18
            degree_level = "Undergraduate / Bachelor's Degree"
        elif any(d in edu_str for d in ['diploma', 'b.com', 'bba']):
            score = 14
            degree_level = "Diploma / Allied Degree"
        elif education:
            score = 10
            degree_level = "General Education"
        else:
            score = 0
            degree_level = "No Education Detected"
            
        return {
            "score": score,
            "max_score": 20,
            "detected_degrees": education,
            "degree_level": degree_level,
            "remarks": f"Detected: {degree_level} ({', '.join(education) if education else 'None'})"
        }

    @classmethod
    def calculate_experience_score(cls, experience_years: float) -> Dict[str, Any]:
        """
        Pillar 3: Professional Experience (Max: 20 pts)
        Evaluates work history, internships, and full-time experience.
        """
        if experience_years >= 3.0:
            score = 20
            exp_label = "3+ Years (Experienced Professional)"
        elif experience_years >= 2.0:
            score = 18
            exp_label = "2+ Years (Mid-level Experience)"
        elif experience_years >= 1.0:
            score = 15
            exp_label = "1+ Year (Junior Professional)"
        elif experience_years >= 0.3:
            score = 12
            exp_label = "Internship / Practical Training"
        else:
            score = 8
            exp_label = "Fresher / Entry Level (Baseline Academic Profile)"
            
        return {
            "score": score,
            "max_score": 20,
            "experience_years": experience_years,
            "level": exp_label,
            "remarks": f"Experience profile: {exp_label}"
        }

    @classmethod
    def calculate_projects_score(cls, raw_text: str, sections: List[str]) -> Dict[str, Any]:
        """
        Pillar 4: Projects & Action Verbs (Max: 15 pts)
        Evaluates project demonstration and impact-driven action verbs.
        """
        lower_text = raw_text.lower()
        has_projects_sec = any('project' in s.lower() for s in sections)
        
        # Count action verbs in the resume
        verbs_found = [verb for verb in cls.ACTION_VERBS if re.search(r'\b' + verb + r'\b', lower_text)]
        verb_count = len(verbs_found)
        
        if has_projects_sec and verb_count >= 5:
            score = 15
            remarks = "Strong project portfolio with impactful action verbs."
        elif has_projects_sec or verb_count >= 4:
            score = 12
            remarks = "Good project presence. Elaborate on measurable impact and technologies."
        elif verb_count >= 2:
            score = 8
            remarks = "Add a dedicated 'Projects' section highlighting full-stack/AI implementations."
        else:
            score = 3
            remarks = "Missing project details. Hands-on projects are critical for tech screening."
            
        return {
            "score": score,
            "max_score": 15,
            "has_projects_section": has_projects_sec,
            "action_verbs_count": verb_count,
            "action_verbs_found": verbs_found[:6],
            "remarks": remarks
        }

    @classmethod
    def calculate_completeness_score(
        cls, contact_info: Dict[str, Any], sections: List[str]
    ) -> Dict[str, Any]:
        """
        Pillar 5: Completeness & Professional Links (Max: 15 pts)
        Evaluates contact details (Email, Phone, LinkedIn, GitHub) and structural sections.
        """
        score = 0
        items = []
        
        # Email (+4 pts)
        if contact_info.get("email"):
            score += 4
            items.append("Email Verified (+4)")
            
        # Phone (+3 pts)
        if contact_info.get("phone"):
            score += 3
            items.append("Phone Number (+3)")
            
        # LinkedIn / GitHub (+4 pts)
        if contact_info.get("linkedin") or contact_info.get("github"):
            score += 4
            items.append("LinkedIn/GitHub Profile (+4)")
            
        # Section structure (+4 pts if >= 4 core sections)
        if len(sections) >= 4:
            score += 4
            items.append("Structured Section Layout (+4)")
        elif len(sections) >= 2:
            score += 2
            items.append("Partial Section Layout (+2)")
            
        return {
            "score": min(score, 15),
            "max_score": 15,
            "details": items,
            "sections_count": len(sections),
            "remarks": f"Completed {len(items)} out of 4 professional profile checks."
        }

    @classmethod
    def generate_suggestions(
        cls,
        skills_res: Dict[str, Any],
        edu_res: Dict[str, Any],
        exp_res: Dict[str, Any],
        proj_res: Dict[str, Any],
        comp_res: Dict[str, Any],
        contact_info: Dict[str, Any]
    ) -> List[str]:
        """Generates actionable suggestions to boost resume score."""
        suggestions = []
        
        if skills_res["score"] < 25:
            suggestions.append("Add more domain-specific technical skills, frameworks, and databases to your Skills section.")
            
        if skills_res["domains_count"] < 3:
            suggestions.append("Broaden your skill diversity across backend, databases, cloud, and testing domains.")
            
        if not contact_info.get("github"):
            suggestions.append("Include your GitHub profile URL to showcase open-source contributions and code repositories.")
            
        if not contact_info.get("linkedin"):
            suggestions.append("Add your LinkedIn profile link to enhance recruiter discoverability.")
            
        if proj_res["score"] < 12:
            suggestions.append("Add 2-3 detailed technical projects with bullet points detailing tools used, architecture, and live links.")
            
        if proj_res["action_verbs_count"] < 4:
            suggestions.append("Use strong action verbs like 'Engineered', 'Architected', 'Deployed', 'Optimized' in project descriptions.")
            
        if not edu_res["detected_degrees"]:
            suggestions.append("Ensure your academic degree (e.g., BCA, B.Tech, MCA) is clearly formatted in an 'Education' section.")
            
        if not suggestions:
            suggestions.append("Your resume meets high industry standards! Continue updating your latest project achievements.")
            
        return suggestions

    @classmethod
    def score_resume(cls, parsed_resume: Dict[str, Any], raw_text: str = "") -> Dict[str, Any]:
        """
        Master scoring method. Computes aggregate score (0-100), letter grade,
        sub-scores, and customized improvement tips.
        """
        skills = parsed_resume.get("skills", [])
        categories = parsed_resume.get("skills_by_category", {})
        education = parsed_resume.get("education", [])
        experience_years = parsed_resume.get("experience_years", 0.0)
        sections = parsed_resume.get("sections_detected", [])
        contact = parsed_resume.get("contact_info", {})
        
        # Calculate sub-scores
        skills_res = cls.calculate_skills_score(skills, categories)
        edu_res = cls.calculate_education_score(education)
        exp_res = cls.calculate_experience_score(experience_years)
        proj_res = cls.calculate_projects_score(raw_text, sections)
        comp_res = cls.calculate_completeness_score(contact, sections)
        
        # Total Aggregate Score (Out of 100)
        total_score = (
            skills_res["score"] +
            edu_res["score"] +
            exp_res["score"] +
            proj_res["score"] +
            comp_res["score"]
        )
        
        # Grade and Rating classification
        if total_score >= 85:
            grade = "A+"
            rating_label = "Excellent (Industry Ready)"
            badge_color = "success"
        elif total_score >= 70:
            grade = "A"
            rating_label = "Good (Competitive Profile)"
            badge_color = "primary"
        elif total_score >= 55:
            grade = "B"
            rating_label = "Moderate (Needs Minor Enhancements)"
            badge_color = "warning"
        else:
            grade = "C"
            rating_label = "Needs Improvement (Missing Key Sections)"
            badge_color = "danger"
            
        suggestions = cls.generate_suggestions(
            skills_res, edu_res, exp_res, proj_res, comp_res, contact
        )
        
        return {
            "total_score": total_score,
            "max_score": 100,
            "grade": grade,
            "rating_label": rating_label,
            "badge_color": badge_color,
            "breakdown": {
                "skills": skills_res,
                "education": edu_res,
                "experience": exp_res,
                "projects": proj_res,
                "completeness": comp_res
            },
            "suggestions": suggestions,
            "formula_explanation": (
                "Total Score (100) = Skills & Diversity (30) + Education (20) + "
                "Experience (20) + Projects & Action Verbs (15) + Completeness (15)"
            )
        }


# Convenient helper
def score_resume_nlp(parsed_resume: Dict[str, Any], raw_text: str = "") -> Dict[str, Any]:
    return ResumeScorer.score_resume(parsed_resume, raw_text)
