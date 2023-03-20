"""This module is used to personalize the admin part of the website."""
from django.contrib import admin
from .models import Program, Session, MuscleGroup, Exercice

# Register your models here.
class ProgramAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'updated_at')

admin.site.register(Program, ProgramAdmin)
admin.site.register(Session)
admin.site.register(MuscleGroup)
admin.site.register(Exercice)
