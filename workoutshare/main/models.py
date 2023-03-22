"""This module is used to specify tables in the database for the main part of the app."""
from datetime import timedelta
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from authentication.models import CustomUser #pylint: disable=E0401
# Create your models here.

class Program(models.Model):
    """This class is used to describe the program the users can add."""
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=255, null=True, blank=True)
    published = models.BooleanField(default=0)
    created_at = models.DateTimeField(editable=True, auto_now_add=True)
    updated_at = models.DateTimeField(editable=True, auto_now=True)

    def __str__(self):
        return self.name

    def session_number(self):
        """This method is used to count the number of session a program have."""
        sessions = Session.objects.filter(program_id=self.id)
        return sessions.count()

    def get_exercice_number(self):
        """This method is used to count the number of exercice a program have."""
        exercice_number = 0
        sessions = Session.objects.filter(program_id=self.id)
        for session in sessions:
            exercice_number += session.exercice_number()
        return exercice_number


class Favorite(models.Model):
    """This class is used to let a user add program to his favorites."""
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Session(models.Model):
    """This class is used to describe the session in the programs users can add."""
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name

    def exercice_number(self):
        """This method is used to count the number of exercice a session have."""
        exercices_of_session = Exercice.objects.filter(session_id=self.id)
        return exercices_of_session.count()
    
    def get_owner(self):
        """This method is used to get the owner of a session."""
        program = Program.objects.get(id=self.program_id.id)
        return program.user_id


class MuscleGroup(models.Model):
    """This class is used to describe the muscle group an exercice work."""
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Exercice(models.Model):
    """This class is used to describe the exercices an user can add."""
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    muscle_group_id = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT)
    name = models.CharField(max_length=45)
    sets = models.IntegerField(default=4, validators=[
        MaxValueValidator(99),
        MinValueValidator(1)
    ])
    reps = models.IntegerField(default=12, validators=[
        MaxValueValidator(999),
        MinValueValidator(1)
    ])
    cool = models.DurationField(default="3:00", validators=[
        MaxValueValidator(timedelta(minutes=9, seconds=59)),
        MinValueValidator(timedelta(minutes=0, seconds=0))
    ])

    def __str__(self):
        return self.name
