from django.db import models
from authentication.models import CustomUser

# Create your models here.

class Program(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)
    description = models.TextField(max_length=255, null=True, blank=True)
    published = models.BooleanField(default=0)

    def __str__(self):
        return self.name
    
    def session_number(self):
        sessions = Session.objects.filter(program_id=self.id)
        return sessions.count()

    def get_exercice_number(self):
        exercice_number = 0
        sessions = Session.objects.filter(program_id=self.id)
        for session in sessions:
            exercice_number += session.exercice_number()
        return exercice_number


class Session(models.Model):
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name
    
    def exercice_number(self):
        exercices_of_session = Exercice.objects.filter(session_id=self.id)
        return exercices_of_session.count()


class MuscleGroup(models.Model):
    name = models.CharField(max_length=25, unique=True)

    def __str__(self):
        return self.name


class Exercice(models.Model):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    muscle_group_id = models.ForeignKey(MuscleGroup, on_delete=models.PROTECT)
    name = models.CharField(max_length=45)
    sets = models.IntegerField(default=4)
    reps = models.IntegerField(default=12)
    load = models.IntegerField(default=0)
    cool = models.DurationField(default=180)

    def __str__(self):
        return self.name
