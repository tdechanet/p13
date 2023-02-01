"""This module is used to specify tables in the database."""
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """This class is used to customize the user model."""
    email = models.EmailField(('Adresse email'), unique=True)
