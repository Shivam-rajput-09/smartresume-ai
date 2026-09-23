"""
SmartResume AI — Baseline Job Matching Engine

Combines TF-IDF Vectorization, Cosine Similarity, and Direct Skill Set Overlap
(Jaccard Intersection) to rank and recommend the Top-N job roles.
"""

from typing import Dict, List, Any, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.dataset_loader import dataset_loader
from config import Config


class JobMatcher:
    """Computes similarity and recommends job roles based on TF-IDF and skill overlap."""
    
    def __init__(self, loader=None):
        self.loader = loader or dataset_loader
        self.jobs = self.loader.get_all_jobs()
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            ngram_range=(1, 2),
            max_features=500
        )
        self.job_corpus = []
        self.job_tfidf_matrix = None
        self._prepare_job_corpus()
        
    def _prepare_job_corpus(self):
        """Constructs rich descriptive text profiles for each job role and fits TF-IDF."""
        self.job_corpus = []
        for job in self.jobs:
            # Combine role title, required skills, preferred skills, and description
            skills_text = " ".join(job["all_skills"])
            combined_text = (
                f"{job['role_name']} {job['category']} {skills_text} "
                f"{job['description']}"
            )
            self.job_corpus.append(combined_text)
            
        if self.job_corpus:
            self.job_tfidf_matrix = self.vectorizer.fit_transform(self.job_corpus)

    def calculate_skill_overlap(
        self, candidate_skills: List[str], job_required_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Calculates direct set intersection overlap between candidate skills
        and mandatory job requirements.
        """
        cand_set = {s.lower().strip() for s in candidate_skills}
        req_set = {s.lower().strip() for s in job_required_skills}
        
        matched_skills = sorted(list(cand_set.intersection(req_set)))
        missing_skills = sorted(list(req_set - cand_set))
        
        overlap_pct = (len(matched_skills) / len(req_set) * 100.0) if req_set else 0.0
        
        return {
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_count": len(matched_skills),
            "required_count": len(req_set),
            "overlap_percentage": round(overlap_pct, 1)
        }

    def match_resume(
        self,
        candidate_skills: List[str],
        resume_text: str = "",
        top_n: int = Config.TOP_N_RECOMMENDATIONS
    ) -> List[Dict[str, Any]]:
        """
        Computes composite match score:
        Composite Match % = 65% (Mandatory Skill Overlap) + 35% (TF-IDF Contextual Cosine Similarity)
        """
        if not self.jobs or self.job_tfidf_matrix is None:
            return []
            
        # 1. Compute TF-IDF Cosine Similarity
        if resume_text.strip():
            resume_vec = self.vectorizer.transform([resume_text])
            tfidf_sims = cosine_similarity(resume_vec, self.job_tfidf_matrix).flatten()
        else:
            # Fallback if raw text is empty: vectorize candidate skills
            skills_text = " ".join(candidate_skills)
            resume_vec = self.vectorizer.transform([skills_text])
            tfidf_sims = cosine_similarity(resume_vec, self.job_tfidf_matrix).flatten()

        results = []
        for idx, job in enumerate(self.jobs):
            # Calculate skill overlap
            overlap_data = self.calculate_skill_overlap(
                candidate_skills, job["required_skills"]
            )
            
            skill_score = overlap_data["overlap_percentage"]
            tfidf_score = round(float(tfidf_sims[idx]) * 100.0, 1)
            
            # Weighted Composite Match Score
            composite_score = round(
                (0.65 * skill_score) + (0.35 * tfidf_score), 1
            )
            
            # Clip between 0 and 100
            composite_score = max(0.0, min(100.0, composite_score))
            
            # Match strength categorization
            if composite_score >= 75:
                match_level = "High Match"
                badge_class = "success"
            elif composite_score >= 50:
                match_level = "Moderate Match"
                badge_class = "warning"
            else:
                match_level = "Low Match"
                badge_class = "secondary"

            results.append({
                "rank": 0,  # Assigned after sorting
                "role_id": job["role_id"],
                "role_name": job["role_name"],
                "category": job["category"],
                "match_percentage": composite_score,
                "skill_overlap_percentage": skill_score,
                "tfidf_similarity_percentage": tfidf_score,
                "match_level": match_level,
                "badge_class": badge_class,
                "matched_skills": overlap_data["matched_skills"],
                "missing_skills": overlap_data["missing_skills"],
                "all_required_skills": job["required_skills"],
                "preferred_skills": job["preferred_skills"],
                "learning_path": job["learning_path"],
                "description": job["description"]
            })

        # Sort descending by match percentage
        results.sort(key=lambda x: x["match_percentage"], reverse=True)
        
        # Assign 1-indexed ranks
        for i, item in enumerate(results, 1):
            item["rank"] = i
            
        return results[:top_n]

    def match_specific_role(
        self, role_id_or_name: Any, candidate_skills: List[str], resume_text: str = ""
    ) -> Optional[Dict[str, Any]]:
        """Computes matching metrics for a single targeted job role."""
        all_matches = self.match_resume(candidate_skills, resume_text, top_n=len(self.jobs))
        for m in all_matches:
            if m["role_id"] == role_id_or_name or m["role_name"].lower() == str(role_id_or_name).lower():
                return m
        return None


# Global matcher instance
job_matcher = JobMatcher()


def match_jobs_baseline(
    candidate_skills: List[str],
    resume_text: str = "",
    top_n: int = Config.TOP_N_RECOMMENDATIONS
) -> List[Dict[str, Any]]:
    return job_matcher.match_resume(candidate_skills, resume_text, top_n)
