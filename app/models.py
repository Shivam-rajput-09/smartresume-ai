"""
SmartResume AI — SQLite Database Models and Operations

Lightweight, zero-overhead SQLite database manager to store candidate
resume scans, extracted NLP profiles, scores, and ML recommendations.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

from config import Config, BASE_DIR


class Database:
    """Manages SQLite database connections and table schemas."""
    
    DB_PATH = Path(BASE_DIR) / 'smartresume.db'

    @classmethod
    def get_connection(cls) -> sqlite3.Connection:
        """Returns a connection to the SQLite database with dict row factory."""
        conn = sqlite3.connect(cls.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    @classmethod
    def init_db(cls):
        """Creates tables and indexes if they do not already exist."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resume_scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                candidate_name TEXT,
                email TEXT,
                phone TEXT,
                linkedin TEXT,
                github TEXT,
                extracted_skills TEXT,
                skills_count INTEGER DEFAULT 0,
                skills_by_category TEXT,
                experience_years REAL DEFAULT 0.0,
                education TEXT,
                sections_detected TEXT,
                resume_score INTEGER DEFAULT 0,
                score_grade TEXT,
                score_rating TEXT,
                score_breakdown TEXT,
                suggestions TEXT,
                ml_predicted_role TEXT,
                ml_confidence REAL DEFAULT 0.0,
                top_recommendations TEXT,
                raw_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()

    @classmethod
    def save_scan(
        cls,
        filename: str,
        parsed_nlp: Dict[str, Any],
        score_data: Dict[str, Any],
        recommendations: List[Dict[str, Any]],
        ml_prediction: Dict[str, Any],
        raw_text: str = ""
    ) -> int:
        """Saves a complete parsed resume scan record into the database."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        contact = parsed_nlp.get("contact_info", {})
        
        cursor.execute('''
            INSERT INTO resume_scans (
                filename, candidate_name, email, phone, linkedin, github,
                extracted_skills, skills_count, skills_by_category,
                experience_years, education, sections_detected,
                resume_score, score_grade, score_rating, score_breakdown, suggestions,
                ml_predicted_role, ml_confidence, top_recommendations,
                raw_text
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            contact.get("name", "Candidate"),
            contact.get("email"),
            contact.get("phone"),
            contact.get("linkedin"),
            contact.get("github"),
            json.dumps(parsed_nlp.get("skills", [])),
            parsed_nlp.get("skills_count", 0),
            json.dumps(parsed_nlp.get("skills_by_category", {})),
            parsed_nlp.get("experience_years", 0.0),
            json.dumps(parsed_nlp.get("education", [])),
            json.dumps(parsed_nlp.get("sections_detected", [])),
            score_data.get("total_score", 0),
            score_data.get("grade", "N/A"),
            score_data.get("rating_label", "N/A"),
            json.dumps(score_data.get("breakdown", {})),
            json.dumps(score_data.get("suggestions", [])),
            ml_prediction.get("predicted_role", "N/A"),
            ml_prediction.get("confidence", 0.0),
            json.dumps(recommendations),
            raw_text
        ))
        
        scan_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return scan_id

    @classmethod
    def get_scan_by_id(cls, scan_id: int) -> Optional[Dict[str, Any]]:
        """Retrieves a single scan record parsed into native Python dictionaries."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM resume_scans WHERE id = ?', (scan_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
            
        data = dict(row)
        # Deserialize JSON fields
        for json_field in [
            'extracted_skills', 'skills_by_category', 'education',
            'sections_detected', 'score_breakdown', 'suggestions',
            'top_recommendations'
        ]:
            if data.get(json_field):
                try:
                    data[json_field] = json.loads(data[json_field])
                except Exception:
                    data[json_field] = []
                    
        return data

    @classmethod
    def get_all_scans(cls, limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves recent resume scans for history tracking."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT id, filename, candidate_name, email, resume_score, score_grade, ml_predicted_role, created_at '
            'FROM resume_scans ORDER BY created_at DESC LIMIT ?',
            (limit,)
        )
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @classmethod
    def delete_scan(cls, scan_id: int) -> bool:
        """Deletes a scan record by ID."""
        conn = cls.get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM resume_scans WHERE id = ?', (scan_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0


# Initialize tables upon module import
Database.init_db()
