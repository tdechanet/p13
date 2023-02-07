"""This module is used to specify how a page is going to behave."""
from django.shortcuts import render
from .models import CustomUser, Program

# Create your views here.

def profile(request):
    """This function is used to show to a user all his programs."""
    # getting the number of followers of the user
    number_of_followers = CustomUser.objects.filter(authors=request.user.id).count()

    # getting the programs of the user
    programs = Program.objects.filter(user_id=request.user.id)

    context = {
        "followers": number_of_followers,
        "programs": programs,
    }

    return render(request, 'main/profile.html', context)
