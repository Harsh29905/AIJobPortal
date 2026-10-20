from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('status/update/<int:application_id>/', views.update_application_status_ajax, name='update_application_status_ajax'),
]
