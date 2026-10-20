from django.db import models
from jobs.models import Job
from candidates.models import CandidateProfile


class Application(models.Model):
    STATUS_CHOICES = (
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    resume_file = models.FileField(upload_to='application_resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    
    # AI-Generated Matching Fields (Feature C)
    match_score = models.FloatField(default=0.0, help_text="AI match score percentage (0-100)")
    matched_skills = models.TextField(blank=True, help_text="Comma-separated matched skills")
    missing_skills = models.TextField(blank=True, help_text="Comma-separated missing skills")
    similarity_explanation = models.TextField(blank=True)

    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'applications'
        unique_together = ('job', 'candidate')
        ordering = ['-applied_at']

    def __str__(self):
        return f"{self.candidate.user.get_full_name() or self.candidate.user.username} -> {self.job.title} ({self.status})"

    def get_matched_skills_list(self):
        if not self.matched_skills:
            return []
        return [s.strip() for s in self.matched_skills.split(',') if s.strip()]

    def get_missing_skills_list(self):
        if not self.missing_skills:
            return []
        return [s.strip() for s in self.missing_skills.split(',') if s.strip()]

    def get_status_badge_class(self):
        mapping = {
            'applied': 'bg-secondary',
            'shortlisted': 'bg-primary',
            'interview': 'bg-info text-dark',
            'rejected': 'bg-danger',
            'hired': 'bg-success',
        }
        return mapping.get(self.status, 'bg-secondary')

    def get_score_badge_class(self):
        if self.match_score >= 75:
            return 'bg-success'
        elif self.match_score >= 50:
            return 'bg-warning text-dark'
        else:
            return 'bg-danger'
