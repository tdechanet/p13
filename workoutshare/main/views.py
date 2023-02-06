from django.shortcuts import render
from authentication.models import CustomUser
from .models import *

# Create your views here.

def profile(request):
    number_of_followers = CustomUser.objects.filter(authors=request.user.id).count() # getting the number of followers of the user
    programs = Program.objects.filter(user_id=request.user.id)

    context = {
        "followers": number_of_followers,
        "programs": programs,
    }

    return render(request, 'main/profile.html', context)
