# 🚀 SmartResume AI

### AI-Powered Resume Analyzer, Job Recommendation & Career Roadmap Platform

<p align="center">
  <a href="https://smartresume-ai-t76q.onrender.com/">
    <img src="https://img.shields.io/badge/🌐_Live_Demo-SmartResume_AI-0d6efd?style=for-the-badge" alt="Live Demo">
  </a>
  <a href="https://github.com/Shivam-rajput-09/smartresume-ai">
    <img src="https://img.shields.io/badge/GitHub-Repository-181717?style=for-the-badge&logo=github" alt="GitHub">
  </a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-Web%20Framework-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Scikit--learn-Machine%20Learning-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/NLTK-NLP-154F5B?style=flat-square" alt="NLTK">
  <img src="https://img.shields.io/badge/Bootstrap-5-7952B3?style=flat-square&logo=bootstrap&logoColor=white" alt="Bootstrap">
  <img src="https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat-square&logo=render&logoColor=black" alt="Render">
</p>

---

## 🌐 Live Demo

### [Launch SmartResume AI](https://smartresume-ai-t76q.onrender.com/)

**Resume Upload → Resume Analysis → Job Recommendations → Skill Gap Analysis → Learning Roadmap**

---

## 📌 Overview

**SmartResume AI** is an intelligent career assistance platform that analyzes resumes, extracts candidate information and skills, recommends suitable job roles, identifies skill gaps, and generates structured learning roadmaps.

It combines **Natural Language Processing, Machine Learning, resume parsing, skill analysis, job-role matching, and roadmap generation** into one web application.

The goal is to transform a static resume into an **actionable career development profile**.

```text
Resume
  ↓
Resume Analysis
  ↓
Candidate Profile
  ↓
Job Recommendations
  ↓
Skill Gap Analysis
  ↓
Learning Roadmap
  ↓
Career Development
```

---

## 🎯 Problem Statement

Job seekers often do not know how strong their resume is, which roles match their current skills, which skills are missing for a target role, or what they should learn next.

Resume analysis, job searching, and skill development are commonly handled with separate tools.

**SmartResume AI** brings these activities together into a single platform.

---

## 💡 Key Features

### 📄 Resume Upload & Parsing

Extracts candidate information including:

- Candidate name
- Email and phone number
- Technical skills
- Education
- Professional information
- Resume content

### 📊 Resume Analysis Dashboard

Provides:

- Resume score
- Candidate profile
- Predicted primary role
- Skill breakdown
- Technical skills
- Academic and professional information
- Improvement suggestions

### 🎯 Job Recommendations

Analyzes extracted skills and profile information to identify suitable job roles.

### 🔍 Skill Gap Analysis

For a selected role, identifies:

- Possessed required skills
- Missing required skills
- Possessed preferred skills
- Missing preferred skills
- Skill match percentage
- Readiness information
- Estimated weeks to bridge the gap
- Prioritized missing skills

### 🗺️ Personalized Learning Roadmap

Generates:

- Official learning path
- Learning milestones
- Focus skills
- Learning goals
- Estimated duration
- Recommended capstone project
- Project description

```text
Current Skills
      ↓
Missing Skills
      ↓
Learning Milestones
      ↓
Capstone Project
      ↓
Target Role
```

### 🕒 Scan History

Provides access to previously analyzed resume scans.

---

## 🔄 Application Workflow

```text
                         ┌────────────────────┐
                         │    Upload Resume   │
                         └──────────┬─────────┘
                                    ↓
                         ┌────────────────────┐
                         │   Resume Parsing   │
                         └──────────┬─────────┘
                                    ↓
                         ┌────────────────────┐
                         │ NLP & Skill        │
                         │ Extraction         │
                         └──────────┬─────────┘
                                    ↓
                       ┌────────────────────────┐
                       │ Resume Analysis &      │
                       │ Candidate Profile      │
                       └────────────┬───────────┘
                                    │
                  ┌─────────────────┼─────────────────┐
                  ↓                 ↓                 ↓
        ┌─────────────────┐ ┌────────────────┐ ┌───────────────┐
        │ Job             │ │ Skill Gap      │ │ Resume        │
        │ Recommendations │ │ Analysis       │ │ Dashboard     │
        └────────┬────────┘ └───────┬────────┘ └───────────────┘
                 │                  ↓
                 │        ┌───────────────────┐
                 │        │ Learning Roadmap  │
                 │        └─────────┬─────────┘
                 └──────────────────↓
                         Career Development
```

---

## 🧠 Machine Learning & NLP

### Natural Language Processing

NLP techniques process resume text and identify:

- Skills
- Keywords
- Candidate information
- Education details
- Professional information

The project uses **NLTK** and Python-based text processing.

### Machine Learning

Machine-learning functionality is used for candidate and job-role analysis.

Model training is supported by:

```text
train_models.py
```

Core libraries include:

- Scikit-learn
- Pandas
- NumPy
- NLTK
- Matplotlib

---

## 🛠️ Technology Stack

### Backend

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Flask | Web application framework |
| Gunicorn | Production WSGI server |

### Machine Learning & Data Processing

| Technology | Purpose |
|---|---|
| Scikit-learn | Machine learning |
| Pandas | Data processing |
| NumPy | Numerical operations |
| NLTK | Natural Language Processing |
| Matplotlib | Data visualization |

### Frontend

| Technology | Purpose |
|---|---|
| HTML5 | Page structure |
| CSS3 | Styling |
| JavaScript | Client-side functionality |
| Bootstrap 5 | Responsive UI |
| Bootstrap Icons | Interface icons |

### Resume & Document Processing

| Technology | Purpose |
|---|---|
| PyPDF2 | PDF processing |
| pdfplumber | PDF text extraction |

### Testing & Automation

| Technology | Purpose |
|---|---|
| Pytest | Automated testing |
| Selenium | Browser automation |
| WebDriver Manager | WebDriver management |

### Deployment

| Technology | Purpose |
|---|---|
| GitHub | Source control |
| Render | Cloud deployment |
| Gunicorn | Production server |

---

## 🏗️ System Architecture

```text
USER
 │
 ▼
FLASK WEB APPLICATION
 ├── Routes
 ├── Jinja2 Templates
 └── Static Assets
 │
 ▼
RESUME PROCESSING
 ├── PDF Parsing
 ├── Text Extraction
 └── NLP Processing
 │
 ▼
ANALYSIS ENGINE
 ├── Resume Analysis
 ├── Job Recommendations
 └── Skill Gap Analysis
 │
 ▼
CAREER ROADMAP ENGINE
 ├── Missing Skills
 ├── Milestones
 └── Capstone Project
 │
 ▼
RESULTS
 ├── Dashboard
 ├── Recommendations
 ├── Skill Gap
 └── Learning Roadmap
```

---

## 📂 Project Structure

```text
smartresume-ai/
│
├── app/
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── upload.html
│   │   ├── dashboard.html
│   │   ├── recommendations.html
│   │   ├── skill_gap.html
│   │   ├── roadmap.html
│   │   └── ...
│   │
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   │
│   ├── routes.py
│   └── ...
│
├── data/
│   └── datasets/
│
├── src/
│   ├── skill_gap.py
│   └── ...
│
├── tests/
│
├── config.py
├── run.py
├── train_models.py
├── verify_setup.py
├── demo_phase2.py
├── demo_phase3.py
├── demo_phase4.py
├── demo_phase5.py
├── demo_phase6.py
├── demo_phase7.py
├── demo_phase8.py
├── demo_phase9.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Directory Description

| File / Directory | Description |
|---|---|
| `app/` | Main Flask application |
| `app/templates/` | Jinja2 HTML templates |
| `app/static/` | CSS and JavaScript assets |
| `src/` | Core processing and analysis logic |
| `data/` | Datasets and supporting data |
| `tests/` | Automated tests |
| `config.py` | Application configuration |
| `run.py` | Flask entry point |
| `train_models.py` | Model training workflow |
| `verify_setup.py` | Setup verification |
| `demo_phase*.py` | Demonstration scripts |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Ignored files |

---

## ⚙️ Installation & Setup

### 1. Clone

```bash
git clone https://github.com/Shivam-rajput-09/smartresume-ai.git
cd smartresume-ai
```

### 2. Create Virtual Environment

**Windows**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Locally

```bash
python run.py
```

Open:

```text
http://127.0.0.1:5000
```

---

## 🖥️ How to Use

1. Open **Analyze Resume**.
2. Upload your resume.
3. Review the generated candidate dashboard.
4. Explore recommended job roles.
5. Select a target role in **Skill Gap Analysis**.
6. Review missing and possessed skills.
7. Open the **Learning Roadmap**.
8. Follow the milestones and recommended capstone project.

---

## 🌐 Deployment

SmartResume AI is deployed using **Render**.

### Production URL

**https://smartresume-ai-t76q.onrender.com/**

### Deployment Flow

```text
Local Development
       ↓
      Git
       ↓
    GitHub
       ↓
    Render
       ↓
Production Web Application
```

### Production Start Command

```bash
gunicorn run:app
```

---

## 🧪 Testing

The project contains a dedicated `tests/` directory.

Run the test suite:

```bash
pytest
```

Browser automation/testing uses:

- Selenium
- WebDriver Manager

---

## 🔐 Configuration & Security

Sensitive configuration values should not be committed.

The `.gitignore` excludes:

```text
.env
venv/
.venv/
__pycache__/
*.pyc
*.db
.pytest_cache/
```

Production secrets should be configured through environment variables.

---

## 📸 Screenshots

Add actual application screenshots to a `screenshots/` directory.

Recommended screenshots:

1. Home Page
2. Resume Upload
3. Resume Analysis Dashboard
4. Job Recommendations
5. Skill Gap Analysis
6. Learning Roadmap
7. Scan History

Example:

```markdown
## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Skill Gap Analysis
![Skill Gap Analysis](screenshots/skill-gap.png)

### Learning Roadmap
![Learning Roadmap](screenshots/roadmap.png)
```

---

## 📊 Current Project Status

| Component | Status |
|---|---|
| Resume Upload | ✅ Completed |
| Resume Parsing | ✅ Completed |
| Resume Analysis | ✅ Completed |
| Candidate Dashboard | ✅ Completed |
| Job Recommendations | ✅ Completed |
| Skill Gap Analysis | ✅ Completed |
| Learning Roadmap | ✅ Completed |
| Scan History | ✅ Completed |
| Flask Backend | ✅ Completed |
| GitHub Repository | ✅ Completed |
| Render Deployment | 🟢 Live |

---

## 🚀 Project Highlights

SmartResume AI demonstrates practical implementation of:

- Full-stack web application development
- Flask backend development
- Jinja2 template-based frontend
- Natural Language Processing
- Machine Learning
- Resume parsing
- Skill extraction
- Job-role matching
- Skill-gap analysis
- Automated learning roadmap generation
- Responsive frontend development
- Automated testing
- Git/GitHub workflow
- Cloud deployment

---

## 🔮 Future Enhancements

Potential improvements include:

- 🤖 AI-powered natural-language resume queries
- 🧠 Semantic skill matching using embeddings
- 📚 Personalized course recommendations
- 🔗 Job-board API integration
- 📊 Advanced career analytics
- 📈 Job-market trend analysis
- 📄 Automated resume improvement suggestions
- 👤 User authentication and personalized profiles
- ☁️ Cloud-based resume/document storage
- 📌 Career progress tracking
- 🎯 More advanced role prediction models
- 🔔 Personalized career and learning reminders

---

## 🎓 Project Purpose

SmartResume AI combines:

**Web Development + Machine Learning + Natural Language Processing + Career Intelligence**

The project focuses on turning resume data into meaningful and actionable career insights.

---

## 👨‍💻 Author

### Shivam Kumar

**Computer Science Student | Full-Stack Developer | Machine Learning Enthusiast**

- **GitHub:** [@Shivam-rajput-09](https://github.com/Shivam-rajput-09)
- **Repository:** [SmartResume AI](https://github.com/Shivam-rajput-09/smartresume-ai)
- **Live Application:** [SmartResume AI](https://smartresume-ai-t76q.onrender.com/)

---

## ⭐ Support

If you find this project useful:

⭐ Star the repository  
🍴 Fork the project  
🐛 Report issues  
💡 Suggest improvements

---

## 📄 License

This project is currently intended for educational and development purposes.

If you plan to distribute or reuse it publicly, add an appropriate open-source license such as the MIT License.
