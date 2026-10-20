from django.contrib import admin
from .models import JobRecommendation


@admin.register(JobRecommendation)
class JobRecommendationAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'job', 'score', 'generated_at')
    list_filter = ('generated_at',)
    search_fields = ('candidate__user__username', 'job__title')
    readonly_fields = ('generated_at',)
