"""
Unit tests for Phase 8: Skill-Gap Analysis and Learning Roadmap Engine
"""

import pytest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.skill_gap import SkillGapEngine, analyze_skill_gap


@pytest.fixture
def gap_engine():
    return SkillGapEngine()


def test_skill_tier_priority():
    assert SkillGapEngine.prioritize_skill("python") == 1
    assert SkillGapEngine.prioritize_skill("sql") == 1
    assert SkillGapEngine.prioritize_skill("django") == 2
    assert SkillGapEngine.prioritize_skill("docker") == 3
    assert SkillGapEngine.prioritize_skill("kubernetes") == 4


def test_skill_gap_partial_match(gap_engine):
    # Candidate with partial skills for Python Developer
    cand_skills = ["python", "sql", "git"]
    gap_result = gap_engine.analyze_gap(cand_skills, "Python Developer")
    
    assert gap_result["role_name"] == "Python Developer"
    assert "python" in gap_result["possessed_required_skills"]
    assert "sql" in gap_result["possessed_required_skills"]
    assert "django" in gap_result["missing_required_skills"]
    assert "flask" in gap_result["missing_required_skills"]
    assert gap_result["match_percentage"] == 50.0
    assert gap_result["estimated_weeks_to_bridge"] > 0
    assert "roadmap" in gap_result
    assert len(gap_result["roadmap"]["milestones"]) >= 2


def test_skill_gap_full_match(gap_engine):
    # Candidate possessing all required skills for QA Engineer
    qa_skills = ["manual testing", "automation testing", "selenium", "pytest", "sql", "test-driven development"]
    gap_result = gap_engine.analyze_gap(qa_skills, "QA Engineer")
    
    assert gap_result["match_percentage"] == 100.0
    assert len(gap_result["missing_required_skills"]) == 0
    assert gap_result["readiness_color"] == "success"


def test_invalid_role_name_handling(gap_engine):
    with pytest.raises(ValueError):
        gap_engine.analyze_gap(["python"], "Non Existent Astronaut Role")


def test_learning_roadmap_structure(gap_engine):
    cand_skills = ["python"]
    gap = analyze_skill_gap(cand_skills, "Machine Learning Engineer")
    
    roadmap = gap["roadmap"]
    assert "milestones" in roadmap
    assert "recommended_capstone" in roadmap
    assert "title" in roadmap["recommended_capstone"]
    assert "desc" in roadmap["recommended_capstone"]
    assert len(roadmap["milestones"]) >= 2
