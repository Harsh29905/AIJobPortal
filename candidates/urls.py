from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
    path('profile/edit/', views.candidate_profile_edit, name='candidate_profile_edit'),
    path('resume/upload/', views.candidate_resume_upload, name='candidate_resume_upload'),
]
