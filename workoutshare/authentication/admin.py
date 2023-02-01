"""This module is used to personalize the admin part of the website."""
from django.contrib import admin
from .models import *

admin.site.register(CustomUser)
admin.site.register(Following)

# Register your models here.
