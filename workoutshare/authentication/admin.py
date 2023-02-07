"""This module is used to personalize the admin part of the website."""
from django.contrib import admin
from .models import CustomUser, Following

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Following)
