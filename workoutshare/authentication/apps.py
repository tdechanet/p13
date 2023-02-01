"""This module is used to configure the app."""
from django.apps import AppConfig

class AuthenticationConfig(AppConfig):
    """This class is used to configure the authentication app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'
