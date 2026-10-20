from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from recruiters.models import RecruiterProfile
from candidates.models import CandidateProfile
from jobs.models import Job, JobSkill
from applications.models import Application

User = get_user_model()


class ApplicationWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Recruiter
        self.r_user = User.objects.create_user(username='rec_app_tester', password='pass', role='recruiter')
        self.recruiter = RecruiterProfile.objects.create(user=self.r_user, company_name='AppTech Corp')
        self.job = Job.objects.create(
            recruiter=self.recruiter,
            title='Python Full Stack Dev',
            location='Chicago, IL',
            status='open',
            description='Build web apps with Django and MySQL.'
        )
        JobSkill.objects.create(job=self.job, skill_name='Python')
        JobSkill.objects.create(job=self.job, skill_name='Django')

        # Candidate
        self.c_user = User.objects.create_user(username='cand_app_tester', password='pass', role='candidate')
        self.candidate = CandidateProfile.objects.create(
            user=self.c_user,
            headline='Junior Python Dev',
            skills='Python, Django, MySQL'
        )

    def test_apply_and_calculate_ai_score(self):
        self.client.login(username='cand_app_tester', password='pass')
        resp = self.client.post(reverse('apply_job', args=[self.job.id]), {
            'cover_letter': 'I am eager to contribute to AppTech.',
        })
        self.assertEqual(resp.status_code, 302)
        app = Application.objects.get(candidate=self.candidate, job=self.job)
        self.assertEqual(app.status, 'applied')
        self.assertGreater(app.match_score, 0)
        self.assertIn('Python', app.matched_skills)

    def test_duplicate_application_prevention(self):
        self.client.login(username='cand_app_tester', password='pass')
        # First application
        self.client.post(reverse('apply_job', args=[self.job.id]), {'cover_letter': 'First try'})
        self.assertEqual(Application.objects.filter(candidate=self.candidate, job=self.job).count(), 1)

        # Attempt duplicate application
        resp2 = self.client.post(reverse('apply_job', args=[self.job.id]), {'cover_letter': 'Duplicate try'})
        # Should redirect back with warning and NOT create duplicate
        self.assertEqual(Application.objects.filter(candidate=self.candidate, job=self.job).count(), 1)

        # Verify DB unique constraint also prevents it
        with self.assertRaises(IntegrityError):
            Application.objects.create(candidate=self.candidate, job=self.job)

    def test_recruiter_status_update(self):
        app = Application.objects.create(candidate=self.candidate, job=self.job, status='applied', match_score=85)
        self.client.login(username='rec_app_tester', password='pass')
        resp = self.client.post(reverse('applicant_detail', args=[app.id]), {
            'status': 'shortlisted'
        })
        self.assertEqual(resp.status_code, 302)
        app.refresh_from_db()
        self.assertEqual(app.status, 'shortlisted')
