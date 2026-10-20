from django.urls import path
from . import views

urlpatterns = [
    path('register/candidate/', views.register_candidate, name='register_candidate'),
    path('register/recruiter/', views.register_recruiter, name='register_recruiter'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_redirect, name='dashboard_redirect'),
    path('settings/', views.profile_settings, name='profile_settings'),
]
