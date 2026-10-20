from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.recruiter_dashboard, name='recruiter_dashboard'),
    path('profile/edit/', views.recruiter_profile_edit, name='recruiter_profile_edit'),
    path('jobs/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('applicants/<int:application_id>/', views.applicant_detail, name='applicant_detail'),
]
