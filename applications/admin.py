from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'status', 'match_score', 'applied_at')
    list_filter = ('status', 'applied_at')
    search_fields = ('candidate__user__username', 'candidate__user__email', 'job__title', 'job__recruiter__company_name')
    readonly_fields = ('match_score', 'matched_skills', 'missing_skills', 'similarity_explanation', 'applied_at', 'updated_at')
