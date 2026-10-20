from django.db import models
from recruiters.models import RecruiterProfile


class Job(models.Model):
    WORK_ARRANGEMENT_CHOICES = (
        ('on_site', 'On-Site'),
        ('hybrid', 'Hybrid'),
        ('remote', 'Remote'),
    )

    EMPLOYMENT_TYPE_CHOICES = (
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
    )

    EXPERIENCE_LEVEL_CHOICES = (
        ('entry', 'Entry Level (0-2 yrs)'),
        ('mid', 'Mid Level (2-5 yrs)'),
        ('senior', 'Senior Level (5+ yrs)'),
        ('lead', 'Lead / Principal'),
    )

    STATUS_CHOICES = (
        ('open', 'Open'),
        ('closed', 'Closed'),
    )

    recruiter = models.ForeignKey(RecruiterProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField(help_text="Detailed job description and responsibilities")
    requirements = models.TextField(blank=True, help_text="Required qualifications and expectations")
    location = models.CharField(max_length=150)
    work_arrangement = models.CharField(max_length=20, choices=WORK_ARRANGEMENT_CHOICES, default='on_site')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default='full_time')
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES, default='mid')
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Annual salary minimum")
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, help_text="Annual salary maximum")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['location']),
            models.Index(fields=['work_arrangement']),
            models.Index(fields=['employment_type']),
        ]

    def __str__(self):
        return f"{self.title} at {self.recruiter.company_name}"

    def get_skills_list(self):
        return list(self.skills.values_list('skill_name', flat=True))

    def skills_as_text(self):
        return ", ".join(self.get_skills_list())

    @property
    def applications_count(self):
        return self.applications.count()


class JobSkill(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)

    class Meta:
        db_table = 'job_skills'
        unique_together = ('job', 'skill_name')

    def __str__(self):
        return f"{self.skill_name} ({self.job.title})"
