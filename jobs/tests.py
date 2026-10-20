from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from recruiters.models import RecruiterProfile
from jobs.models import Job, JobSkill

User = get_user_model()


class JobManagementAndSearchTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='rec_tester', password='pass', role='recruiter')
        self.recruiter = RecruiterProfile.objects.create(
            user=self.user,
            company_name='TestTech Global',
            company_location='Seattle, WA'
        )
        self.job1 = Job.objects.create(
            recruiter=self.recruiter,
            title='Django Backend Developer',
            location='Seattle, WA',
            work_arrangement='remote',
            employment_type='full_time',
            experience_level='mid',
            min_salary=100000,
            max_salary=120000,
            description='Build scalable APIs using Django and MySQL.',
            status='open'
        )
        JobSkill.objects.create(job=self.job1, skill_name='Python')
        JobSkill.objects.create(job=self.job1, skill_name='Django')
        JobSkill.objects.create(job=self.job1, skill_name='MySQL')

        self.job2 = Job.objects.create(
            recruiter=self.recruiter,
            title='React Frontend Specialist',
            location='New York, NY',
            work_arrangement='on_site',
            employment_type='contract',
            experience_level='senior',
            description='Build frontend UI in React.',
            status='open'
        )
        JobSkill.objects.create(job=self.job2, skill_name='React')
        JobSkill.objects.create(job=self.job2, skill_name='JavaScript')

    def test_job_search_by_skill_and_title(self):
        resp = self.client.get(reverse('job_list') + '?q=Django')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django Backend Developer')
        self.assertNotContains(resp, 'React Frontend Specialist')

        resp2 = self.client.get(reverse('job_list') + '?q=React')
        self.assertEqual(resp2.status_code, 200)
        self.assertContains(resp2, 'React Frontend Specialist')
        self.assertNotContains(resp2, 'Django Backend Developer')

    def test_job_filter_by_arrangement(self):
        resp = self.client.get(reverse('job_list') + '?work_arrangement=remote')
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Django Backend Developer')
        self.assertNotContains(resp, 'React Frontend Specialist')

    def test_recruiter_can_create_and_toggle_job(self):
        self.client.login(username='rec_tester', password='pass')
        resp = self.client.post(reverse('job_create'), {
            'title': 'Cloud DevOps Architect',
            'location': 'Seattle, WA',
            'work_arrangement': 'remote',
            'employment_type': 'full_time',
            'experience_level': 'senior',
            'min_salary': 140000,
            'max_salary': 175000,
            'status': 'open',
            'skills_input': 'AWS, Docker, Kubernetes, Linux',
            'description': 'Manage high-reliability cloud infrastructure.',
            'requirements': 'Extensive AWS and Kubernetes experience.',
        })
        self.assertEqual(resp.status_code, 302)
        new_job = Job.objects.get(title='Cloud DevOps Architect')
        self.assertEqual(new_job.skills.count(), 4)

        # Toggle status to closed
        self.client.get(reverse('job_toggle_status', args=[new_job.id]))
        new_job.refresh_from_db()
        self.assertEqual(new_job.status, 'closed')
