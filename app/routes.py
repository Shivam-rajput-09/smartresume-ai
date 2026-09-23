"""
SmartResume AI — Flask Web Application Routes & Controllers

Handles web views, resume upload pipelines, analysis dashboards,
job recommendations, skill-gap analysis, and REST API endpoints.
"""

import os
import json
from pathlib import Path
from flask import (
    Blueprint, render_template, request, redirect, url_for,
    flash, jsonify, current_app, abort
)
from werkzeug.utils import secure_filename

from app.models import Database
from src.extractor import ResumeExtractor, extract_resume_text, ResumeExtractorError
from src.nlp_preprocessor import parse_resume_nlp
from src.scorer import score_resume_nlp
from src.matcher import match_jobs_baseline
from src.ml_recommender import predict_job_role_ml
from src.skill_gap import analyze_skill_gap
from src.dataset_loader import dataset_loader

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home landing page with system overview and features."""
    recent_scans = Database.get_all_scans(limit=5)
    total_roles = len(dataset_loader.get_all_jobs())
    total_skills = len(dataset_loader.get_all_known_skills())
    return render_template(
        'index.html',
        recent_scans=recent_scans,
        total_roles=total_roles,
        total_skills=total_skills
    )


@main_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """Handles resume document upload, text parsing, scoring, and matching."""
    if request.method == 'POST':
        # Check if file part is in request
        if 'resume' not in request.files:
            flash('No file uploaded. Please select a resume file (.pdf, .txt).', 'danger')
            return redirect(request.url)
            
        file = request.files['resume']
        if file.filename == '':
            flash('No file selected. Please choose a valid file.', 'warning')
            return redirect(request.url)
            
        if not ResumeExtractor.is_allowed_file(file.filename):
            flash('Invalid file format. Please upload a .PDF or .TXT resume document.', 'danger')
            return redirect(request.url)
            
        filename = secure_filename(file.filename)
        upload_folder = Path(current_app.config['UPLOAD_FOLDER'])
        upload_folder.mkdir(parents=True, exist_ok=True)
        file_path = upload_folder / filename
        file.save(str(file_path))
        
        try:
            # 1. Text Extraction
            extraction_res = extract_resume_text(file_path)
            raw_text = extraction_res["text"]
            
            # 2. NLP Preprocessing & Entity/Skill Extraction
            parsed_nlp = parse_resume_nlp(raw_text)
            
            # 3. Transparent Resume Scoring
            score_data = score_resume_nlp(parsed_nlp, raw_text)
            
            # 4. Baseline Job Matching (TF-IDF + Skill Overlap)
            top_recommendations = match_jobs_baseline(
                parsed_nlp["skills"], raw_text, top_n=current_app.config['TOP_N_RECOMMENDATIONS']
            )
            
            # 5. Machine Learning Role Classification
            ml_prediction = predict_job_role_ml(parsed_nlp["skills"], top_n=3)
            
            # 6. Save Scan Record to SQLite Database
            scan_id = Database.save_scan(
                filename=filename,
                parsed_nlp=parsed_nlp,
                score_data=score_data,
                recommendations=top_recommendations,
                ml_prediction=ml_prediction,
                raw_text=raw_text
            )
            
            # Remove temporary uploaded file to conserve storage
            try:
                os.remove(file_path)
            except Exception:
                pass
                
            flash('Resume analyzed successfully!', 'success')
            return redirect(url_for('main.dashboard', scan_id=scan_id))
            
        except ResumeExtractorError as e:
            flash(f'Extraction Error: {str(e)}', 'danger')
            return redirect(request.url)
        except Exception as e:
            flash(f'An unexpected error occurred during analysis: {str(e)}', 'danger')
            return redirect(request.url)

    return render_template('upload.html')


@main_bp.route('/dashboard/<int:scan_id>')
def dashboard(scan_id):
    """Resume Analysis Dashboard displaying score, contact, skills, and summary."""
    scan = Database.get_scan_by_id(scan_id)
    if not scan:
        flash('Requested scan record was not found.', 'warning')
        return redirect(url_for('main.index'))
        
    return render_template('dashboard.html', scan=scan)


@main_bp.route('/recommendations/<int:scan_id>')
def recommendations(scan_id):
    """Top 5 Job Recommendations and ML Classification Confidence Page."""
    scan = Database.get_scan_by_id(scan_id)
    if not scan:
        flash('Requested scan record was not found.', 'warning')
        return redirect(url_for('main.index'))
        
    # Re-run live ML predictions for detailed probability breakdown
    ml_data = predict_job_role_ml(scan.get("extracted_skills", []), top_n=5)
    
    return render_template(
        'recommendations.html',
        scan=scan,
        recommendations=scan.get("top_recommendations", []),
        ml_data=ml_data
    )


@main_bp.route('/skill-gap/<int:scan_id>/<role_identifier>')
def skill_gap(scan_id, role_identifier):
    """Targeted Skill-Gap Analysis for a selected job role."""
    scan = Database.get_scan_by_id(scan_id)
    if not scan:
        flash('Requested scan record was not found.', 'warning')
        return redirect(url_for('main.index'))
        
    try:
        # Check if role_identifier is role_id or role_name
        if role_identifier.isdigit():
            role_arg = int(role_identifier)
        else:
            role_arg = role_identifier
            
        gap_data = analyze_skill_gap(scan.get("extracted_skills", []), role_arg)
        all_roles = dataset_loader.get_all_jobs()
        
        return render_template(
            'skill_gap.html',
            scan=scan,
            gap=gap_data,
            all_roles=all_roles,
            current_role_id=gap_data["role_id"]
        )
    except Exception as e:
        flash(f'Error analyzing skill gap: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard', scan_id=scan_id))


@main_bp.route('/roadmap/<int:scan_id>/<role_identifier>')
def roadmap(scan_id, role_identifier):
    """Interactive Learning Roadmap and Capstone Project recommendation."""
    scan = Database.get_scan_by_id(scan_id)
    if not scan:
        flash('Requested scan record was not found.', 'warning')
        return redirect(url_for('main.index'))
        
    try:
        if role_identifier.isdigit():
            role_arg = int(role_identifier)
        else:
            role_arg = role_identifier
            
        gap_data = analyze_skill_gap(scan.get("extracted_skills", []), role_arg)
        
        return render_template(
            'roadmap.html',
            scan=scan,
            gap=gap_data,
            roadmap=gap_data["roadmap"]
        )
    except Exception as e:
        flash(f'Error generating roadmap: {str(e)}', 'danger')
        return redirect(url_for('main.dashboard', scan_id=scan_id))


@main_bp.route('/history')
def history():
    """Scan History tracking all previous resume analyses."""
    scans = Database.get_all_scans(limit=100)
    return render_template('history.html', scans=scans)


@main_bp.route('/delete/<int:scan_id>', methods=['POST'])
def delete_scan(scan_id):
    """Deletes a scan record."""
    Database.delete_scan(scan_id)
    flash('Scan record deleted successfully.', 'info')
    return redirect(url_for('main.history'))


# ---------------- REST API ENDPOINTS ----------------

@main_bp.route('/api/analyze-text', methods=['POST'])
def api_analyze_text():
    """Headless REST API to analyze raw resume text directly via JSON."""
    data = request.get_json(silent=True)
    if not data or 'text' not in data:
        return jsonify({"error": "Missing 'text' key in JSON request body."}), 400
        
    raw_text = data['text'].strip()
    if not raw_text:
        return jsonify({"error": "Provided resume text is empty."}), 400
        
    parsed_nlp = parse_resume_nlp(raw_text)
    score_data = score_resume_nlp(parsed_nlp, raw_text)
    recs = match_jobs_baseline(parsed_nlp["skills"], raw_text, top_n=5)
    ml_pred = predict_job_role_ml(parsed_nlp["skills"], top_n=3)
    
    return jsonify({
        "status": "success",
        "parsed_nlp": parsed_nlp,
        "score_data": score_data,
        "recommendations": recs,
        "ml_prediction": ml_pred
    }), 200


@main_bp.route('/api/scan/<int:scan_id>', methods=['GET'])
def api_get_scan(scan_id):
    """REST API returning complete parsed JSON for a specific scan ID."""
    scan = Database.get_scan_by_id(scan_id)
    if not scan:
        return jsonify({"error": "Scan record not found."}), 404
    return jsonify({"status": "success", "scan": scan}), 200
