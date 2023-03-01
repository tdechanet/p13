"""This module is used to specify the urls accessible to the user."""
from django.urls import path

from . import views

APP_NAME = 'main'

urlpatterns = [
    path('home/', views.home, name='home'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('program/<int:program_id>/', views.program, name='program'),
    path('program/<int:program_id>/delete/', views.delete_program, name='delete_program'),
    path('session/<int:session_id>/delete/', views.delete_session, name='delete_session'),
]
