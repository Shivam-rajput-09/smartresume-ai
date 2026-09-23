"""
Generates standard sample PDF resumes for automated testing and demonstrations.
Uses matplotlib's built-in PDF backend (no extra external PDF generator required).
"""

from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def create_sample_pdf(output_path: Path, title: str, content_lines: list):
    fig = plt.figure(figsize=(8.5, 11))
    fig.clf()
    
    y_pos = 0.95
    line_height = 0.026
    
    # Title / Header
    plt.text(0.08, y_pos, title, fontsize=15, fontweight='bold', family='sans-serif')
    y_pos -= 0.04
    
    for line in content_lines:
        if line.startswith("==="):
            plt.text(0.08, y_pos, line.replace("=", "").strip(), fontsize=12, fontweight='bold', color='#1a365d')
            y_pos -= line_height * 1.2
        elif line.strip() == "":
            y_pos -= line_height * 0.6
        else:
            plt.text(0.08, y_pos, line, fontsize=9.5, family='monospace' if ':' in line else 'sans-serif')
            y_pos -= line_height
            
    plt.axis('off')
    
    with PdfPages(output_path) as pdf:
        pdf.savefig(fig, bbox_inches='tight')
    plt.close(fig)
    print(f"[+] Successfully generated sample PDF: {output_path.name}")

if __name__ == "__main__":
    resumes_dir = Path(__file__).resolve().parent
    
    # 1. Sample Python Dev PDF
    py_lines = [
        "Email: rohit.verma@example.com | Phone: +91 9988776655 | Bengaluru, India",
        "",
        "=== SUMMARY",
        "Python Developer with strong experience in Flask, Django, SQL, and REST APIs.",
        "Passionate about backend architectures, PostgreSQL, and Docker containerization.",
        "",
        "=== SKILLS",
        "Languages: Python, JavaScript, SQL, C++",
        "Frameworks: Django, Flask, FastAPI, Pandas, NumPy",
        "Databases: PostgreSQL, MySQL, Redis",
        "Tools & Cloud: Git, Docker, Linux, AWS, Postman",
        "Testing: Pytest, Unit Testing, Automation Testing, Agile",
        "",
        "=== EDUCATION",
        "Bachelor of Computer Applications (BCA AI) - 2024",
        "",
        "=== PROJECTS",
        "- Inventory Management Backend: Built RESTful API with Flask, SQLAlchemy, SQLite.",
        "- Web Scraper Pipeline: Automated data ingestion using Python, BeautifulSoup and Celery.",
        "",
        "=== EXPERIENCE",
        "Backend Intern - AlphaTech (6 Months)",
        "- Developed API endpoints and integrated Redis cache."
    ]
    create_sample_pdf(resumes_dir / "sample_python_developer.pdf", "ROHIT VERMA - PYTHON DEVELOPER", py_lines)
    
    # 2. Sample QA Engineer PDF
    qa_lines = [
        "Email: ananya.singh@example.com | Phone: +91 9811223344 | Delhi, India",
        "",
        "=== SUMMARY",
        "QA Automation Engineer skilled in Selenium WebDriver, Python, Pytest, and Manual Testing.",
        "Experienced in designing automated test suites, test cases, Postman API testing, and JIRA.",
        "",
        "=== SKILLS",
        "Testing: Automation Testing, Manual Testing, Selenium, Pytest, Test-Driven Development",
        "Tools: Postman, JIRA, Git, CI/CD, Jenkins, Chrome DevTools",
        "Languages & DB: Python, Java, SQL, MySQL",
        "",
        "=== EDUCATION",
        "BCA in Artificial Intelligence (2021 - 2024)",
        "",
        "=== PROJECTS",
        "- E-Commerce Automated Test Suite: Created end-to-end regression tests using Selenium & Pytest.",
        "- Banking API Testing: Automated 40+ REST API test scenarios using Postman and Newman.",
        "",
        "=== EXPERIENCE",
        "QA Intern - QualityFirst Labs (1 Year)",
        "- Executed positive, negative, and boundary test cases for web applications."
    ]
    create_sample_pdf(resumes_dir / "sample_qa_engineer.pdf", "ANANYA SINGH - QA AUTOMATION ENGINEER", qa_lines)
