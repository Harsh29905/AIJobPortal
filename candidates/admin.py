from django.contrib import admin
from .models import CandidateProfile


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'headline', 'current_location', 'preferred_location', 'experience_years', 'updated_at')
    search_fields = ('user__username', 'user__email', 'headline', 'skills', 'extracted_skills')
    list_filter = ('experience_years', 'preferred_location')
