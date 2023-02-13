"""This module is used to specify the urls accessible to the user."""
from django.urls import path

from . import views

APP_NAME = 'main'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('profile/<int:program_id>/delete/', views.delete_program, name='delete_program'),
]
