from django.contrib import admin
from .models import RecruiterProfile


@admin.register(RecruiterProfile)
class RecruiterProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'company_location', 'industry', 'contact_email', 'created_at')
    search_fields = ('company_name', 'user__username', 'industry', 'company_location')
    list_filter = ('industry',)
