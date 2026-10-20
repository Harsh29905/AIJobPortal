import re
from typing import Dict, List, Set, Tuple
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Comprehensive Skill Catalog for Feature A & C
SKILL_CATALOG = [
    # Programming Languages
    "Python", "Java", "C", "C++", "C#", "JavaScript", "TypeScript", "PHP", "Ruby",
    "Go", "Golang", "Rust", "Kotlin", "Swift", "R", "Dart", "Scala", "Perl",
    "HTML", "HTML5", "CSS", "CSS3", "SASS", "SQL", "Bash", "Shell",

    # Web & Backend Frameworks
    "Django", "Flask", "FastAPI", "React", "React.js", "Angular", "Vue.js", "Vue",
    "Node.js", "Express", "Express.js", "Next.js", "Nuxt.js", "Spring", "Spring Boot",
    "ASP.NET", ".NET", "Laravel", "Ruby on Rails", "Bootstrap", "Tailwind CSS", "jQuery",

    # Databases & Caching
    "MySQL", "PostgreSQL", "SQLite", "MongoDB", "Redis", "Oracle", "Microsoft SQL Server",
    "Cassandra", "DynamoDB", "Firebase", "Elasticsearch", "Neo4j",

    # Cloud, DevOps & Tools
    "AWS", "Azure", "Google Cloud", "GCP", "Docker", "Kubernetes", "Git", "GitHub",
    "GitLab", "CI/CD", "Jenkins", "Linux", "Unix", "Nginx", "Apache", "Terraform",
    "Ansible", "Jira", "Postman",

    # AI, Data Science & Machine Learning
    "Machine Learning", "Deep Learning", "Natural Language Processing", "NLP",
    "Computer Vision", "Scikit-Learn", "TensorFlow", "PyTorch", "Keras", "Pandas",
    "NumPy", "Matplotlib", "Seaborn", "Data Analysis", "Data Science", "OpenCV",
    "Large Language Models", "LLMs",

    # Core Software Engineering & Methodologies
    "REST API", "RESTful APIs", "GraphQL", "Microservices", "Object-Oriented Programming",
    "OOP", "Agile", "Scrum", "Test-Driven Development", "TDD", "Unit Testing",
    "System Design", "Algorithms", "Data Structures"
]

# Aliases and normalization mapping
SKILL_ALIASES = {
    "golang": "Go",
    "react.js": "React",
    "reactjs": "React",
    "vuejs": "Vue.js",
    "vue": "Vue.js",
    "node": "Node.js",
    "nodejs": "Node.js",
    "expressjs": "Express",
    "spring-boot": "Spring Boot",
    "aws": "AWS",
    "gcp": "Google Cloud",
    "llm": "Large Language Models",
    "llms": "Large Language Models",
    "rest": "REST API",
    "restful": "REST API",
    "restful api": "REST API",
    "restful apis": "REST API",
    "rest api": "REST API",
    "rest apis": "REST API",
    "nlp": "Natural Language Processing",
    "ml": "Machine Learning",
}


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts raw text from a PDF file (FileField or file path) using pypdf.
    Handles multi-page documents and suppresses formatting noise.
    """
    text_chunks = []
    try:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text_chunks.append(extracted)
    except Exception as e:
        return f""
    return "\n".join(text_chunks).strip()


def normalize_skill_name(skill: str) -> str:
    cleaned = skill.strip()
    lowered = cleaned.lower()
    return SKILL_ALIASES.get(lowered, cleaned)


def extract_skills_from_text(text: str) -> List[str]:
    """
    Feature A: Resume Skill Extraction
    Extracts recognized technical and professional skills from raw text using boundary matching.
    """
    if not text:
        return []

    found_skills: Set[str] = set()
    cleaned_text = " " + text.lower() + " "

    for skill in SKILL_CATALOG:
        escaped_skill = re.escape(skill.lower())
        # Word boundary pattern ensuring accurate matches (e.g., prevents "C" from matching "Cat")
        if skill.lower() in ["c", "r"]:
            pattern = r'(?<=[\s,;.()\/-])' + escaped_skill + r'(?=[\s,;.()\/-])'
        elif "+" in skill:
            pattern = r'(?:^|[\s,;.()\/-])' + re.escape(skill.lower()) + r'(?=[\s,;.()\/-]|$)'
        else:
            pattern = r'\b' + escaped_skill + r'\b'

        if re.search(pattern, cleaned_text, re.IGNORECASE):
            norm = normalize_skill_name(skill)
            found_skills.add(norm)

    return sorted(list(found_skills), key=lambda x: x.lower())


def calculate_resume_job_match(resume_text: str, candidate_skills: List[str], job) -> Dict:
    """
    Feature C: Resume-to-Job Match Score
    Calculates a comprehensive, explainable match score percentage (0-100)
    between a candidate's profile/resume and a job vacancy.
    """
    job_required_skills = [normalize_skill_name(s) for s in job.get_skills_list()]
    
    # Extract skills from resume text if provided
    extracted_from_resume = extract_skills_from_text(resume_text) if resume_text else []
    
    # Merge all candidate skills
    all_candidate_skills_set = {
        normalize_skill_name(s).lower() for s in (candidate_skills + extracted_from_resume) if s
    }

    # Analyze matched vs missing skills
    matched_skills = []
    missing_skills = []
    for req in job_required_skills:
        if req.lower() in all_candidate_skills_set:
            matched_skills.append(req)
        else:
            missing_skills.append(req)

    # 1. Skill Match Component (60% weight)
    if job_required_skills:
        skill_score = (len(matched_skills) / len(job_required_skills)) * 100.0
    else:
        # If no specific required skills listed, neutral score
        skill_score = 75.0

    # 2. Text / Semantic Similarity Component using TF-IDF & Cosine Similarity (40% weight)
    candidate_corpus = (
        (resume_text or "") + " " + " ".join(candidate_skills) + " " + " ".join(extracted_from_resume)
    ).strip()
    job_corpus = (
        f"{job.title} {job.description} {job.requirements} " + " ".join(job_required_skills)
    ).strip()

    semantic_score = 0.0
    if candidate_corpus and job_corpus:
        try:
            vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
            tfidf_matrix = vectorizer.fit_transform([candidate_corpus, job_corpus])
            cos_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            # Scale cosine similarity (typical ranges 0.05-0.60) to a realistic 0-100 scale
            semantic_score = min(100.0, max(0.0, float(cos_sim * 140.0)))
        except Exception:
            semantic_score = skill_score

    # Composite Match Score calculation
    # 65% weighted skill match, 35% semantic text similarity
    composite_score = (0.65 * skill_score) + (0.35 * semantic_score)
    final_score = round(min(100.0, max(10.0, composite_score)), 1)

    # Build human-readable explainability summary
    if job_required_skills:
        explanation = (
            f"Candidate matches {len(matched_skills)} of {len(job_required_skills)} required skills "
            f"({round(skill_score, 1)}% skill overlap). "
            f"Matched: {', '.join(matched_skills) if matched_skills else 'None'}. "
            f"Missing: {', '.join(missing_skills) if missing_skills else 'None'}. "
            f"Text similarity score: {round(semantic_score, 1)}%."
        )
    else:
        explanation = f"General profile match based on text content: {round(semantic_score, 1)}%."

    return {
        'score': final_score,
        'matched_skills': matched_skills,
        'missing_skills': missing_skills,
        'skill_score': round(skill_score, 1),
        'semantic_score': round(semantic_score, 1),
        'explanation': explanation,
    }


def get_job_recommendations_for_candidate(candidate_profile, limit: int = 10) -> List[Dict]:
    """
    Feature B: Job Recommendation System
    Recommends open jobs matching candidate's profile skills, resume text, and location preferences
    using TF-IDF cosine similarity and weighted skill overlap.
    """
    from jobs.models import Job

    open_jobs = list(Job.objects.filter(status='open').prefetch_related('skills', 'recruiter'))
    if not open_jobs:
        return []

    candidate_skills = candidate_profile.get_all_skills_list()
    resume_text = candidate_profile.extracted_resume_text or ""
    candidate_location = (candidate_profile.preferred_location or candidate_profile.current_location or "").lower()

    scored_jobs = []
    for job in open_jobs:
        match_data = calculate_resume_job_match(resume_text, candidate_skills, job)
        base_score = match_data['score']

        # Location Match Bonus (up to +10%)
        job_loc = job.location.lower()
        if job.work_arrangement == 'remote':
            base_score = min(100.0, base_score + 8.0)
        elif candidate_location and candidate_location in job_loc:
            base_score = min(100.0, base_score + 10.0)

        match_data['job'] = job
        match_data['total_score'] = round(base_score, 1)
        scored_jobs.append(match_data)

    # Sort descending by calculated score
    scored_jobs.sort(key=lambda x: x['total_score'], reverse=True)
    return scored_jobs[:limit]
