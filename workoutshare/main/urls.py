"""This module is used to specify the urls accessible to the user."""
from django.urls import path

from . import views

APP_NAME = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('legal-mention', views.legal_mention, name='legal-mention'),
    path('favorite/', views.favorite, name='favorite'),
    path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('program/<int:program_id>/', views.program, name='program'),
    path('program/<int:program_id>/delete/', views.delete_program, name='delete_program'),
    path('session/<int:session_id>/', views.session, name='session'),
    path('session/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    path('research/', views.user_research, name='research'),
    path('exercice/<int:exercice_id>/delete/', views.delete_exercice, name='delete_exercice'),
    path('session/<int:session_id>/exercice/', views.new_exercice, name='new_exercice'),
]
