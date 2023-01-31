from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model

from .forms import SignUpForm


User = get_user_model()

def test(request):
    return render(request, 'registration/test.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            login(request, user)
            return redirect('/login')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
