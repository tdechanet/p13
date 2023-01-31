"""This module is used to specify how a page is going to behave."""
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model

from .forms import SignUpForm


User = get_user_model()

def signup(request):
    """This function is used to signup an user in the application."""
    if request.method == 'POST': #looking if user send the form
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save() #checking that the form is valid
            return redirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
