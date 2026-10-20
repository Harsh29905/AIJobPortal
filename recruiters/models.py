from django.db import models
from django.conf import settings


class RecruiterProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recruiter_profile')
    company_name = models.CharField(max_length=255)
    company_website = models.URLField(blank=True)
    company_description = models.TextField(blank=True)
    company_location = models.CharField(max_length=150, blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_logo = models.FileField(upload_to='company_logos/', blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'recruiter_profiles'
        verbose_name = 'Recruiter Profile'
        verbose_name_plural = 'Recruiter Profiles'

    def __str__(self):
        return f"{self.company_name} ({self.user.username})"

    def active_jobs_count(self):
        return self.jobs.filter(status='open').count()

    def total_applications_count(self):
        from applications.models import Application
        return Application.objects.filter(job__recruiter=self).count()
