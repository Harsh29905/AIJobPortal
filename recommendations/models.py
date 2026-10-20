from django.db import models
from candidates.models import CandidateProfile
from jobs.models import Job


class JobRecommendation(models.Model):
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='recommendations')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='recommended_for')
    score = models.FloatField(default=0.0, help_text="Calculated match score percentage (0-100)")
    matched_skills = models.TextField(blank=True, help_text="Comma-separated matched skills")
    generated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'job_recommendations'
        unique_together = ('candidate', 'job')
        ordering = ['-score', '-generated_at']

    def __str__(self):
        return f"Recommendation: {self.candidate.user.username} -> {self.job.title} ({self.score:.1f}%)"

    def get_matched_skills_list(self):
        if not self.matched_skills:
            return []
        return [s.strip() for s in self.matched_skills.split(',') if s.strip()]
