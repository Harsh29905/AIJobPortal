# AI-Powered Job Portal Using Django and MySQL

> **MVP Version 1.0** · Comprehensive implementation of the Product Requirements Document (PRD).

A modern, responsive web application built with **Django**, **MySQL**, **Bootstrap 5**, and local **Python NLP/Scikit-Learn** AI algorithms that connects job seekers with recruiters, extracts technical skills from resumes, recommends matching opportunities, and computes explainable applicant match scores.

---

## 🚀 Key Features

### 1. Role-Based Architecture & Authentication
- **Job Seeker (`candidate`)**: Create and update profile, specify skills, education, experience, and location preferences; upload PDF resume for automated AI skill extraction; search/filter jobs; receive AI job recommendations; apply for jobs with duplicate-submission protection; track application statuses.
- **Recruiter / Employer (`recruiter`)**: Manage company profile; publish, edit, toggle open/close, and delete job openings; view candidates ranked by AI Match Score; review matched and missing skills breakdown; change candidate status (`applied`, `shortlisted`, `interview`, `hired`, `rejected`).
- **Administrator (`admin`)**: Comprehensive management & moderation via Django Admin (`/admin/`).

### 2. AI-Powered Engine (Local & Explainable)
- **Feature A — Resume Skill Extraction**:
  - Uses `pypdf` to extract text from candidate PDF resumes.
  - Matches technical & professional skills using regular expressions and a 150+ keyword catalog (Python, Django, MySQL, Docker, React, AWS, etc.).
- **Feature B — Job Recommendation Engine**:
  - Evaluates candidate profile skills and resume corpus against all active jobs.
  - Computes composite suitability: **60%** skill overlap (Jaccard / coverage ratio) + **30%** semantic similarity (TF-IDF vectorizer + Cosine Similarity) + **10%** location match bonus.
- **Feature C — Resume-to-Job Match Score & Breakdown**:
  - Calculates a transparent 0–100% match percentage for every applicant.
  - Detailed breakdown of **Matched Skills** (green badges) and **Missing Skills** (red badges).
  - Clear explainability text with disclaimer: *"The match score is an estimate of similarity, not a prediction of candidate performance. Recruiter review required."*

### 3. Search, Filter & Responsive UI
- Search across job titles, descriptions, skills, and companies.
- Server-side filtering by **Work Arrangement** (On-site, Hybrid, Remote), **Employment Type** (Full-time, Part-time, Internship, Contract), and **Experience Level**.
- Pagination (6 jobs per page) preserving filter parameters across pagination links.
- Lightweight, modern Bootstrap 5 UI with neutral background, subtle card elevation, and responsive design.

---

## 🏗️ Project Architecture

```
ai_job_portal/
├── manage.py
├── requirements.txt
├── .env.example
├── .env
├── README.md
├── job_portal/             # Project settings & URL routing
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/               # Custom User model, auth & roles
├── candidates/             # Candidate profiles & resume upload
├── recruiters/             # Company profiles & recruiter dashboard
├── jobs/                   # Job listings, search, filters & CRUD
├── applications/           # Job applications & status management
├── recommendations/        # AI Service (TF-IDF, Cosine Sim, Skill Parser)
├── templates/              # Bootstrap 5 HTML templates
│   ├── base.html
│   ├── accounts/
│   ├── candidates/
│   ├── recruiters/
│   ├── jobs/
│   ├── applications/
│   └── recommendations/
├── static/                 # Custom CSS & lightweight JS
└── media/                  # Uploaded PDF resumes & logos
```

---

## 🗄️ Database Setup (MySQL & SQLite)

The application fully supports **MySQL** (via `pymysql`) and falls back to **SQLite** for instant zero-configuration development:

### Connecting to MySQL
1. Ensure your MySQL server is running (e.g., MySQL 8.0 / 8.4 on port `3306` or `3307`).
2. Create the database:
   ```sql
   CREATE DATABASE job_portal_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. Update `.env` (or set environment variables):
   ```env
   DB_ENGINE=mysql
   DB_NAME=job_portal_db
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3307
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```

---

## ⚡ Quickstart Guide

### 1. Clone / Navigate to Project Directory
```bash
cd C:\Users\Mihir\.gemini\antigravity\scratch\ai_job_portal
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Apply Migrations
```bash
python manage.py migrate
```

### 4. Load Sample Data (Optional)
Populate realistic candidates, recruiters, jobs, and applications with precomputed AI scores:
```bash
python manage.py seed_data
```

### 5. Run the Development Server
```bash
python manage.py runserver 127.0.0.1:8000
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 👥 Demo Accounts (Seeded)

| Role | Username | Password | Notes |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Django Admin access at `/admin/` |
| **Recruiter** | `techcorp_recruiter` | `pass123` | TechCorp Systems (Enterprise SaaS) |
| **Recruiter** | `cloudscale_recruiter`| `pass123` | CloudScale AI (AI & Machine Learning) |
| **Candidate** | `alex_candidate` | `pass123` | Senior Python/Django Dev (84.8% match for Python roles) |
| **Candidate** | `sarah_candidate`| `pass123` | Full Stack React Dev (85.1% match for Full Stack) |
| **Candidate** | `marcus_candidate`| `pass123`| ML & NLP Specialist (83.9% match for ML role) |

---

## 🧪 Running the Automated Test Suite

Run the full automated test suite verifying permissions, job searches, duplicate prevention, and AI scoring:
```bash
python manage.py test
```

---

## 🛡️ Acceptance Criteria Validation

- [x] **Registration & Authentication**: Separate registration for Job Seekers and Recruiters with role-based routing.
- [x] **Job Management**: Recruiters can create, edit, close, and delete vacancies.
- [x] **Search & Filters**: Multi-criteria search by title, skill, location, employment type, and work arrangement with pagination.
- [x] **Duplicate Prevention**: Database unique constraint and view-level validation prevent duplicate applications.
- [x] **Feature A (Skill Extraction)**: NLP regex boundary matching recognizes skills from PDF resumes or text.
- [x] **Feature B (Job Recommendations)**: TF-IDF vectorization and cosine similarity rank jobs for candidates.
- [x] **Feature C (Match Score Breakdown)**: Displays matched skills, missing skills, semantic score, and explainability text.
