from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from candidates.models import CandidateProfile
from recruiters.models import RecruiterProfile
from jobs.models import Job, JobSkill
from applications.models import Application
from recommendations.services import calculate_resume_job_match

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds realistic sample data for candidates, recruiters, jobs, and applications'

    def handle(self, *args, **options):
        self.stdout.write("Starting database seeding...")

        # 1. Superuser
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@jobportal.ai', 'admin123')
            admin.role = 'admin'
            admin.first_name = 'Portal'
            admin.last_name = 'Administrator'
            admin.save()
            self.stdout.write(self.style.SUCCESS("Created Superuser: admin / admin123"))

        # 2. Recruiters
        recruiters_data = [
            {
                'username': 'techcorp_recruiter',
                'email': 'recruiter@techcorp.io',
                'first_name': 'David',
                'last_name': 'Chen',
                'company_name': 'TechCorp Systems',
                'company_website': 'https://techcorp.io',
                'company_location': 'San Francisco, CA',
                'industry': 'Enterprise Cloud & SaaS',
                'company_description': 'TechCorp Systems builds next-generation enterprise SaaS solutions serving Fortune 500 companies worldwide.',
            },
            {
                'username': 'cloudscale_recruiter',
                'email': 'hiring@cloudscale.ai',
                'first_name': 'Elena',
                'last_name': 'Rostova',
                'company_name': 'CloudScale AI',
                'company_website': 'https://cloudscale.ai',
                'company_location': 'New York, NY',
                'industry': 'Artificial Intelligence & Machine Learning',
                'company_description': 'Pioneering production AI systems, distributed feature stores, and automated model governance platforms.',
            },
            {
                'username': 'fintech_recruiter',
                'email': 'careers@paynexus.com',
                'first_name': 'James',
                'last_name': 'Wilson',
                'company_name': 'PayNexus Global',
                'company_website': 'https://paynexus.com',
                'company_location': 'Austin, TX',
                'industry': 'Financial Technology',
                'company_description': 'Next-gen payment rails and high-throughput real-time settlement infrastructure.',
            }
        ]

        created_recruiters = {}
        for r_info in recruiters_data:
            user, created = User.objects.get_or_create(username=r_info['username'], defaults={
                'email': r_info['email'],
                'first_name': r_info['first_name'],
                'last_name': r_info['last_name'],
                'role': 'recruiter'
            })
            if created:
                user.set_password('pass123')
                user.save()
            
            profile, _ = RecruiterProfile.objects.get_or_create(user=user, defaults={
                'company_name': r_info['company_name'],
                'company_website': r_info['company_website'],
                'company_location': r_info['company_location'],
                'industry': r_info['industry'],
                'contact_email': r_info['email'],
                'company_description': r_info['company_description']
            })
            created_recruiters[r_info['company_name']] = profile
            self.stdout.write(f"Recruiter ready: {user.username} ({profile.company_name})")

        # 3. Jobs & Skills
        jobs_data = [
            {
                'recruiter': created_recruiters['TechCorp Systems'],
                'title': 'Senior Python / Django Backend Engineer',
                'location': 'San Francisco, CA (or Remote)',
                'work_arrangement': 'remote',
                'employment_type': 'full_time',
                'experience_level': 'senior',
                'min_salary': 130000,
                'max_salary': 165000,
                'description': 'We are seeking an experienced Backend Engineer to architect and scale our core Django REST services, optimize MySQL queries, and deploy containerized services via Docker and Kubernetes.',
                'requirements': '5+ years experience with Python and Django. Strong proficiency with MySQL database design, indexing, and optimization. Hands-on experience with Docker, Redis caching, and CI/CD pipelines.',
                'skills': ['Python', 'Django', 'MySQL', 'Docker', 'REST API', 'Redis', 'Linux']
            },
            {
                'recruiter': created_recruiters['CloudScale AI'],
                'title': 'Machine Learning & NLP Research Engineer',
                'location': 'New York, NY',
                'work_arrangement': 'hybrid',
                'employment_type': 'full_time',
                'experience_level': 'mid',
                'min_salary': 125000,
                'max_salary': 155000,
                'description': 'Join our NLP research team to design, evaluate, and deploy text analysis models, embedding retrieval systems, and predictive transformers.',
                'requirements': 'Proficiency with Python, Scikit-Learn, PyTorch, and NLP tokenization libraries. Experience with Pandas, data preprocessing, and model evaluation metrics.',
                'skills': ['Python', 'Machine Learning', 'Natural Language Processing', 'Scikit-Learn', 'PyTorch', 'Pandas', 'NumPy']
            },
            {
                'recruiter': created_recruiters['PayNexus Global'],
                'title': 'Full Stack React & Python Developer',
                'location': 'Austin, TX',
                'work_arrangement': 'hybrid',
                'employment_type': 'full_time',
                'experience_level': 'mid',
                'min_salary': 110000,
                'max_salary': 140000,
                'description': 'Build responsive user dashboards using React and Bootstrap, coupled with clean Django REST APIs handling high-volume transaction history.',
                'requirements': '3+ years full-stack development experience. Solid understanding of React, JavaScript/TypeScript, Python, HTML5, CSS3, and relational databases.',
                'skills': ['Python', 'Django', 'React', 'JavaScript', 'HTML', 'CSS', 'PostgreSQL', 'REST API']
            },
            {
                'recruiter': created_recruiters['TechCorp Systems'],
                'title': 'DevOps & Cloud Infrastructure Specialist',
                'location': 'San Francisco, CA',
                'work_arrangement': 'on_site',
                'employment_type': 'full_time',
                'experience_level': 'senior',
                'min_salary': 135000,
                'max_salary': 170000,
                'description': 'Lead our cloud reliability, infrastructure-as-code automation, and container orchestration across multi-region AWS environments.',
                'requirements': 'Deep expertise with AWS, Docker, Kubernetes, Terraform, and CI/CD pipelines. Strong Linux systems administration skills.',
                'skills': ['AWS', 'Docker', 'Kubernetes', 'Linux', 'Terraform', 'CI/CD', 'Git']
            },
            {
                'recruiter': created_recruiters['CloudScale AI'],
                'title': 'Junior Data Analyst & Python Intern',
                'location': 'New York, NY',
                'work_arrangement': 'remote',
                'employment_type': 'internship',
                'experience_level': 'entry',
                'min_salary': 45000,
                'max_salary': 60000,
                'description': 'An exciting internship opportunity for recent graduates or students passionate about Python, SQL queries, data exploration, and dashboard reporting.',
                'requirements': 'Basic knowledge of Python, SQL queries, Pandas, and data visualization tools. Enthusiastic problem-solver.',
                'skills': ['Python', 'SQL', 'Pandas', 'Data Analysis', 'Git']
            },
            {
                'recruiter': created_recruiters['PayNexus Global'],
                'title': 'MySQL Database Administrator (DBA)',
                'location': 'Austin, TX',
                'work_arrangement': 'remote',
                'employment_type': 'full_time',
                'experience_level': 'senior',
                'min_salary': 120000,
                'max_salary': 150000,
                'description': 'Ensure ultra-reliable uptime, replication, replication lag mitigation, schema migrations, and query tuning for critical MySQL clusters.',
                'requirements': 'Proven background tuning MySQL parameters, InnoDB buffer pools, replication topologies, and backup recovery.',
                'skills': ['MySQL', 'SQL', 'Linux', 'Database Administration', 'Performance Tuning', 'Bash']
            }
        ]

        created_jobs = []
        for j_info in jobs_data:
            job, created = Job.objects.get_or_create(
                recruiter=j_info['recruiter'],
                title=j_info['title'],
                defaults={
                    'location': j_info['location'],
                    'work_arrangement': j_info['work_arrangement'],
                    'employment_type': j_info['employment_type'],
                    'experience_level': j_info['experience_level'],
                    'min_salary': j_info['min_salary'],
                    'max_salary': j_info['max_salary'],
                    'description': j_info['description'],
                    'requirements': j_info['requirements'],
                    'status': 'open',
                }
            )
            job.skills.all().delete()
            for s in j_info['skills']:
                JobSkill.objects.create(job=job, skill_name=s)
            created_jobs.append(job)
            self.stdout.write(f"Job created: {job.title} ({j_info['recruiter'].company_name})")

        # 4. Candidates & Profiles
        candidates_data = [
            {
                'username': 'alex_candidate',
                'email': 'alex.dev@gmail.com',
                'first_name': 'Alex',
                'last_name': 'Morales',
                'headline': 'Senior Python / Django Backend Developer',
                'current_location': 'San Francisco, CA',
                'preferred_location': 'Remote or San Francisco',
                'experience_years': 6,
                'skills': 'Python, Django, MySQL, Docker, REST API, Linux, Redis, Git',
                'education': 'B.S. in Computer Science, UC Berkeley, 2019',
                'bio': 'Passionate backend architect specializing in scalable Python web services, MySQL database schema optimization, and Docker orchestration.'
            },
            {
                'username': 'sarah_candidate',
                'email': 'sarah.miller@outlook.com',
                'first_name': 'Sarah',
                'last_name': 'Miller',
                'headline': 'Full Stack Developer | React & Python',
                'current_location': 'Austin, TX',
                'preferred_location': 'Austin or Remote',
                'experience_years': 4,
                'skills': 'React, JavaScript, Python, Django, HTML, CSS, PostgreSQL, REST API',
                'education': 'B.S. in Software Engineering, UT Austin, 2021',
                'bio': 'Versatile developer bridging clean frontend UI in React with robust backend APIs in Django.'
            },
            {
                'username': 'marcus_candidate',
                'email': 'marcus.ai@gmail.com',
                'first_name': 'Marcus',
                'last_name': 'Vance',
                'headline': 'Machine Learning Engineer & NLP Specialist',
                'current_location': 'New York, NY',
                'preferred_location': 'New York',
                'experience_years': 3,
                'skills': 'Python, Machine Learning, Natural Language Processing, Scikit-Learn, PyTorch, Pandas, NumPy, Data Analysis',
                'education': 'M.S. in Data Science, Columbia University, 2022',
                'bio': 'Dedicated to building production ML models, TF-IDF and semantic embeddings, and automated text analysis pipelines.'
            }
        ]

        created_candidates = []
        for c_info in candidates_data:
            user, created = User.objects.get_or_create(username=c_info['username'], defaults={
                'email': c_info['email'],
                'first_name': c_info['first_name'],
                'last_name': c_info['last_name'],
                'role': 'candidate'
            })
            if created:
                user.set_password('pass123')
                user.save()

            profile, _ = CandidateProfile.objects.get_or_create(user=user, defaults={
                'headline': c_info['headline'],
                'current_location': c_info['current_location'],
                'preferred_location': c_info['preferred_location'],
                'experience_years': c_info['experience_years'],
                'skills': c_info['skills'],
                'education': c_info['education'],
                'bio': c_info['bio'],
                'extracted_skills': c_info['skills'],
                'extracted_resume_text': f"Resume of {c_info['first_name']} {c_info['last_name']}.\n"
                                        f"Title: {c_info['headline']}\n"
                                        f"Skills: {c_info['skills']}\n"
                                        f"Experience: {c_info['experience_years']} years\n"
                                        f"Bio: {c_info['bio']}\n"
                                        f"Education: {c_info['education']}\n"
            })
            created_candidates.append(profile)
            self.stdout.write(f"Candidate ready: {user.username} ({profile.headline})")

        # 5. Initial Applications with AI Match Scores
        # Alex applies to Senior Python Django Engineer & Full Stack Engineer
        sample_applications = [
            (created_candidates[0], created_jobs[0], 'shortlisted', 'I have 6 years building high-throughput Django systems with MySQL.'),
            (created_candidates[0], created_jobs[2], 'interview', 'Excited about the full-stack opportunity combining React and Python.'),
            (created_candidates[1], created_jobs[2], 'shortlisted', 'My strong React and Python expertise aligns perfectly with PayNexus.'),
            (created_candidates[2], created_jobs[1], 'interview', 'My research in NLP and machine learning makes this role a great match.'),
            (created_candidates[2], created_jobs[4], 'applied', 'Eager to contribute my Python and Pandas skills.')
        ]

        for cand, job, status, cover_letter in sample_applications:
            if not Application.objects.filter(candidate=cand, job=job).exists():
                match_res = calculate_resume_job_match(
                    cand.extracted_resume_text,
                    cand.get_all_skills_list(),
                    job
                )
                Application.objects.create(
                    candidate=cand,
                    job=job,
                    cover_letter=cover_letter,
                    status=status,
                    match_score=match_res['score'],
                    matched_skills=", ".join(match_res['matched_skills']),
                    missing_skills=", ".join(match_res['missing_skills']),
                    similarity_explanation=match_res['explanation']
                )
                self.stdout.write(f"Application created: {cand.user.username} -> {job.title} (Match: {match_res['score']}%)")

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
