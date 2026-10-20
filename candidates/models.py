from django.db import models
from django.conf import settings


class CandidateProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='candidate_profile')
    headline = models.CharField(max_length=255, blank=True, help_text="e.g. Python Full Stack Developer | Django & Cloud")
    phone = models.CharField(max_length=25, blank=True)
    current_location = models.CharField(max_length=120, blank=True)
    preferred_location = models.CharField(max_length=120, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    education = models.TextField(blank=True, help_text="Degree, Institution, Year of Graduation")
    skills = models.TextField(blank=True, help_text="Comma-separated skills (e.g. Python, Django, MySQL, REST APIs)")
    bio = models.TextField(blank=True, help_text="Brief professional summary")
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    extracted_resume_text = models.TextField(blank=True)
    extracted_skills = models.TextField(blank=True, help_text="AI extracted skills from resume")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'candidate_profiles'
        verbose_name = 'Candidate Profile'
        verbose_name_plural = 'Candidate Profiles'

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} Profile"

    def get_manual_skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]

    def get_extracted_skills_list(self):
        if not self.extracted_skills:
            return []
        return [s.strip() for s in self.extracted_skills.split(',') if s.strip()]

    def get_all_skills_list(self):
        combined = set()
        for s in self.get_manual_skills_list():
            combined.add(s)
        for s in self.get_extracted_skills_list():
            combined.add(s)
        return sorted(list(combined), key=lambda x: x.lower())

    def profile_completion_percentage(self):
        score = 0
        total_parts = 6
        if self.headline:
            score += 1
        if self.current_location or self.preferred_location:
            score += 1
        if self.skills or self.extracted_skills:
            score += 1
        if self.education:
            score += 1
        if self.bio:
            score += 1
        if self.resume_file:
            score += 1
        return int((score / total_parts) * 100)
