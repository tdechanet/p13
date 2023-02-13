"""This module is used to configure the app."""
from django.apps import AppConfig


class MainConfig(AppConfig):
    """This class is used to configure the main app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'
