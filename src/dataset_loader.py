"""
SmartResume AI — Dataset Loader & Manager Module

Provides high-level utilities to load, clean, normalize, search,
and dynamically extend the job roles dataset and domain skills taxonomy.
"""

import json
import csv
from pathlib import Path
from typing import Dict, List, Set, Optional, Any
import pandas as pd

from config import Config


class DatasetLoader:
    """Manages loading and querying job roles and skill taxonomy."""
    
    def __init__(
        self,
        jobs_csv_path: Optional[Path] = None,
        skills_json_path: Optional[Path] = None
    ):
        self.jobs_csv_path = jobs_csv_path or Config.JOB_DATASET_CSV
        self.skills_json_path = skills_json_path or Config.SKILLS_DATASET_JSON
        
        self._skills_data: Dict[str, Any] = {}
        self._aliases: Dict[str, str] = {}
        self._categories: Dict[str, List[str]] = {}
        self._all_skills_cache: Set[str] = set()
        
        self.load_skills_taxonomy()
        
    def load_skills_taxonomy(self) -> Dict[str, Any]:
        """Loads and parses the hierarchical skills JSON dataset."""
        if not self.skills_json_path.exists():
            raise FileNotFoundError(f"Skills dataset not found at: {self.skills_json_path}")
            
        with open(self.skills_json_path, 'r', encoding='utf-8') as f:
            self._skills_data = json.load(f)
            
        self._categories = self._skills_data.get("categories", {})
        self._aliases = self._skills_data.get("skill_aliases", {})
        
        # Build flattened set of all normalized skills
        self._all_skills_cache = set()
        for cat, skills in self._categories.items():
            for skill in skills:
                self._all_skills_cache.add(skill.lower().strip())
                
        for alias, canonical in self._aliases.items():
            self._all_skills_cache.add(alias.lower().strip())
            self._all_skills_cache.add(canonical.lower().strip())
            
        return self._skills_data

    def normalize_skill(self, skill_name: str) -> str:
        """
        Normalizes a skill name by trimming whitespace, lowercasing,
        and resolving aliases (e.g. 'js' -> 'javascript').
        """
        cleaned = skill_name.strip().lower()
        return self._aliases.get(cleaned, cleaned)

    def get_all_known_skills(self) -> Set[str]:
        """Returns all known unique canonical and alias skills."""
        return self._all_skills_cache

    def get_skill_categories(self) -> Dict[str, List[str]]:
        """Returns the dictionary of skill categories."""
        return self._categories

    def load_jobs_df(self) -> pd.DataFrame:
        """Loads the job roles dataset as a pandas DataFrame."""
        if not self.jobs_csv_path.exists():
            raise FileNotFoundError(f"Job roles dataset not found at: {self.jobs_csv_path}")
            
        df = pd.read_csv(self.jobs_csv_path)
        return df

    def get_all_jobs(self) -> List[Dict[str, Any]]:
        """
        Loads and returns all job roles as structured dictionaries
        with normalized skills lists.
        """
        df = self.load_jobs_df()
        jobs = []
        for _, row in df.iterrows():
            req_skills = [
                self.normalize_skill(s)
                for s in str(row['required_skills']).split(',')
                if s.strip()
            ]
            pref_skills = [
                self.normalize_skill(s)
                for s in str(row['preferred_skills']).split(',')
                if s.strip()
            ]
            
            jobs.append({
                "role_id": int(row['role_id']),
                "role_name": str(row['role_name']).strip(),
                "category": str(row['category']).strip(),
                "required_skills": req_skills,
                "preferred_skills": pref_skills,
                "all_skills": list(dict.fromkeys(req_skills + pref_skills)),
                "min_experience_years": int(row.get('min_experience_years', 0)),
                "description": str(row['description']).strip(),
                "learning_path": str(row['learning_path']).strip()
            })
        return jobs

    def get_role_by_id(self, role_id: int) -> Optional[Dict[str, Any]]:
        """Finds a specific job role by its numeric ID."""
        for job in self.get_all_jobs():
            if job["role_id"] == role_id:
                return job
        return None

    def get_role_by_name(self, role_name: str) -> Optional[Dict[str, Any]]:
        """Finds a job role by exact or case-insensitive name."""
        target = role_name.strip().lower()
        for job in self.get_all_jobs():
            if job["role_name"].lower() == target:
                return job
        return None

    def add_custom_job_role(
        self,
        role_name: str,
        category: str,
        required_skills: List[str],
        preferred_skills: List[str],
        description: str,
        learning_path: str,
        min_experience_years: int = 0
    ) -> Dict[str, Any]:
        """
        Dynamically appends a new job role to the CSV dataset.
        Demonstrates system extensibility.
        """
        df = self.load_jobs_df()
        next_id = int(df['role_id'].max()) + 1 if not df.empty else 1
        
        req_str = ", ".join([s.strip().lower() for s in required_skills])
        pref_str = ", ".join([s.strip().lower() for s in preferred_skills])
        
        new_row = {
            "role_id": next_id,
            "role_name": role_name.strip(),
            "category": category.strip(),
            "required_skills": req_str,
            "preferred_skills": pref_str,
            "min_experience_years": min_experience_years,
            "description": description.strip(),
            "learning_path": learning_path.strip()
        }
        
        # Append to CSV
        with open(self.jobs_csv_path, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(new_row.keys()))
            writer.writerow(new_row)
            
        return self.get_role_by_id(next_id)


# Global singleton instance for easy import across modules
dataset_loader = DatasetLoader()
