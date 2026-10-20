from django.contrib import admin
from .models import Job, JobSkill


class JobSkillInline(admin.TabularInline):
    model = JobSkill
    extra = 1


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'recruiter', 'location', 'work_arrangement', 'employment_type', 'experience_level', 'status', 'created_at')
    list_filter = ('status', 'work_arrangement', 'employment_type', 'experience_level', 'created_at')
    search_fields = ('title', 'description', 'recruiter__company_name', 'location')
    inlines = [JobSkillInline]


@admin.register(JobSkill)
class JobSkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'job')
    search_fields = ('skill_name', 'job__title')
