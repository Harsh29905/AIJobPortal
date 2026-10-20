from django.test import TestCase
from django.contrib.auth import get_user_model
from recruiters.models import RecruiterProfile
from candidates.models import CandidateProfile
from jobs.models import Job, JobSkill
from recommendations.services import (
    extract_skills_from_text,
    calculate_resume_job_match,
    get_job_recommendations_for_candidate,
)

User = get_user_model()


class AIServiceTests(TestCase):
    def setUp(self):
        self.r_user = User.objects.create_user(username='ai_rec', password='pwd', role='recruiter')
        self.recruiter = RecruiterProfile.objects.create(user=self.r_user, company_name='AILabs Inc')
        
        # Job 1: Python/Django/MySQL
        self.job1 = Job.objects.create(
            recruiter=self.recruiter,
            title='Senior Backend Developer',
            location='San Francisco, CA',
            work_arrangement='remote',
            status='open',
            description='We need a Python developer who knows Django, MySQL, Docker, and REST APIs.',
            requirements='Must have 4+ years of backend development.'
        )
        for s in ['Python', 'Django', 'MySQL', 'Docker', 'REST API']:
            JobSkill.objects.create(job=self.job1, skill_name=s)

        # Job 2: Frontend React
        self.job2 = Job.objects.create(
            recruiter=self.recruiter,
            title='Frontend UI Engineer',
            location='New York, NY',
            work_arrangement='on_site',
            status='open',
            description='Build frontend components using React and TypeScript.',
            requirements='Proficient in JavaScript, CSS, and modern web frameworks.'
        )
        for s in ['React', 'TypeScript', 'JavaScript', 'HTML', 'CSS']:
            JobSkill.objects.create(job=self.job2, skill_name=s)

        # Candidate
        self.c_user = User.objects.create_user(username='ai_cand', password='pwd', role='candidate')
        self.candidate = CandidateProfile.objects.create(
            user=self.c_user,
            headline='Backend Python Architect',
            skills='Python, Django, MySQL, Docker',
            preferred_location='Remote'
        )

    def test_feature_a_skill_extraction(self):
        sample_resume_text = """
        John Doe
        Experienced software engineer specializing in Python and Django backend architecture.
        Hands-on experience maintaining MySQL relational databases, writing RESTful APIs,
        and containerizing microservices with Docker and Kubernetes. Proficient with Git and Linux.
        """
        extracted = extract_skills_from_text(sample_resume_text)
        self.assertIn('Python', extracted)
        self.assertIn('Django', extracted)
        self.assertIn('MySQL', extracted)
        self.assertIn('Docker', extracted)
        self.assertIn('Kubernetes', extracted)
        self.assertIn('Linux', extracted)
        self.assertIn('REST API', extracted)

    def test_feature_b_job_recommendation_ranking(self):
        recs = get_job_recommendations_for_candidate(self.candidate)
        self.assertTrue(len(recs) >= 2)
        # Job 1 should rank higher than Job 2 because candidate has Python, Django, MySQL, Docker
        self.assertEqual(recs[0]['job'], self.job1)
        self.assertGreater(recs[0]['total_score'], recs[1]['total_score'])

    def test_feature_c_resume_to_job_match_score(self):
        match_data = calculate_resume_job_match(
            resume_text="Experienced with Python, Django, and MySQL databases.",
            candidate_skills=['Python', 'Django', 'MySQL'],
            job=self.job1
        )
        # Job 1 requires: Python, Django, MySQL, Docker, REST API
        self.assertIn('Python', match_data['matched_skills'])
        self.assertIn('Django', match_data['matched_skills'])
        self.assertIn('MySQL', match_data['matched_skills'])
        self.assertIn('Docker', match_data['missing_skills'])
        self.assertIn('REST API', match_data['missing_skills'])
        self.assertGreater(match_data['score'], 50.0)
        self.assertTrue(len(match_data['explanation']) > 10)
