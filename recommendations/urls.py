from django.urls import path
from . import views

urlpatterns = [
    path('recommended/', views.recommendations_list, name='recommendations_list'),
]
