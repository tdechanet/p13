"""This module is used to specify the urls accessible to the user."""
from django.urls import path

from . import views

APP_NAME = 'main'

urlpatterns = [
    path('', views.home_page, name='home'),
    path('legal-mention/', views.legal_mention, name='legal-mention'),
    path('favorite/', views.favorite_page, name='favorite'),
    path('profile/', views.profile_page, name='profile'),
    path('profile/<int:user_id>/', views.profile_page, name='profile'),
    path('program/<int:program_id>/', views.program_page, name='program'),
    path('program/<int:program_id>/delete/', views.delete_program_page, name='delete_program'),
    path('session/<int:session_id>/', views.session_page, name='session'),
    path('session/<int:session_id>/delete/', views.delete_session_page, name='delete_session'),
    path('research/', views.user_research_page, name='research'),
    path('exercice/<int:exercice_id>/delete/', views.delete_exercice_page, name='delete_exercice'),
    path('session/<int:session_id>/exercice/', views.new_exercice_page, name='new_exercice'),
]
