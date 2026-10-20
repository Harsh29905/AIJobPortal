# AI-Powered Job Portal Using Django and MySQL

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
core Breakdown)**: Displays matched skills, missing skills, semantic score, and explainability text.
