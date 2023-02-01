from django.db import models
from authentication.models import CustomUser

# Create your models here.

class Program(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)
    description = models.TextField(max_length=255, null=True, blank=True)
    published = models.BooleanField(default=0)

    def __str__(self):
        return self.name


class Session(models.Model):
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.name


class MuscleGroup(models.Model):
    name = models.CharField(max_length=45, unique=True)

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
