"""This module is used to personalize the admin part of the website."""
from django.contrib import admin
from .models import CustomUser

admin.site.register(CustomUser)

# Register your models here.
