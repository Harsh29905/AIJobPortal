from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from candidates.models import CandidateProfile
from recruiters.models import RecruiterProfile

User = get_user_model()


class AuthenticationAndRoleTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_candidate_registration(self):
        response = self.client.post(reverse('register_candidate'), {
            'username': 'john_dev',
            'email': 'john@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'headline': 'Python Developer',
            'skills': 'Python, Django, MySQL',
            'experience_years': 3,
            'preferred_location': 'Remote',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='john_dev')
        self.assertTrue(user.is_candidate)
        self.assertFalse(user.is_recruiter)
        self.assertTrue(hasattr(user, 'candidate_profile'))
        self.assertEqual(user.candidate_profile.experience_years, 3)

    def test_recruiter_registration(self):
        response = self.client.post(reverse('register_recruiter'), {
            'username': 'acme_recruiter',
            'email': 'hiring@acme.com',
            'first_name': 'Alice',
            'last_name': 'Smith',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
            'company_name': 'Acme Corporation',
            'company_website': 'https://acme.com',
            'company_location': 'Boston, MA',
            'industry': 'Software',
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='acme_recruiter')
        self.assertTrue(user.is_recruiter)
        self.assertFalse(user.is_candidate)
        self.assertTrue(hasattr(user, 'recruiter_profile'))
        self.assertEqual(user.recruiter_profile.company_name, 'Acme Corporation')

    def test_role_based_dashboard_redirect(self):
        cand = User.objects.create_user(username='cand1', password='pass', role='candidate')
        self.client.login(username='cand1', password='pass')
        resp = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(resp, reverse('candidate_dashboard'))

        rec = User.objects.create_user(username='rec1', password='pass', role='recruiter')
        self.client.login(username='rec1', password='pass')
        resp2 = self.client.get(reverse('dashboard_redirect'))
        self.assertRedirects(resp2, reverse('recruiter_dashboard'))

    def test_unauthorized_access_restriction(self):
        cand = User.objects.create_user(username='cand2', password='pass', role='candidate')
        CandidateProfile.objects.create(user=cand)
        self.client.login(username='cand2', password='pass')
        # Candidate should NOT be allowed to access recruiter dashboard
        resp = self.client.get(reverse('recruiter_dashboard'))
        self.assertRedirects(resp, reverse('dashboard_redirect'), target_status_code=302)
