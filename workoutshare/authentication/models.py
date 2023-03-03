"""This module is used to specify tables in the database for the authencation part of the app."""
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """This class is used to customize the user model."""
    username = models.CharField(('Nom d\'utilisateur'), max_length=25, unique=True)
    email = models.EmailField(('Adresse email'), unique=True)

    def followers_number(self):
        """This method is used to count the number of followers a user have."""
        followers = Following.objects.filter(author=self.pk)
        return followers.count()


class Following(models.Model):
    """This class is used to let a user follower another user."""
    author = models.ForeignKey(CustomUser, related_name="authors", on_delete=models.CASCADE)
    follower = models.ForeignKey(CustomUser, related_name="followers", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author} is followed by {self.follower}"
