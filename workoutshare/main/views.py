"""This module is used to specify how a page is going to behave."""
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Program, Session, Exercice

# Create your views here.

@login_required(login_url='/login/')
def profile(request):
    """This function is used to show to a user all his programs."""

    # getting the number of followers of the user
    number_of_followers = CustomUser.objects.filter(authors=request.user.id).count()

    # getting the programs of the user
    programs = Program.objects.filter(user_id=request.user.id).order_by('name')

    if request.method == 'POST':

        # pointing to the right program
        program_id = request.POST.get('id')
        program = programs[int(program_id)]

        if 'program_publish' in request.POST:
            form = request.POST.get('program_publish')

            # reverse published state
            if form == "True":
                program.published = False
            else:
                program.published = True

            program.save()

        # redirect to delete url
        if 'program_delete' in request.POST:
            return HttpResponseRedirect(f'{program.id}/delete/')

    context = {
        "followers": number_of_followers,
        "programs": programs,
    }

    return render(request, 'main/profile.html', context)


def delete_program(request, program_id):
    """This function is used to permit a user to delete his programs."""
    program = get_object_or_404(Program, id=program_id) # getting program

    if program.user_id == request.user: # verifying that the program belong to the connected user
        program.delete()

    # redirect to the profile
    return redirect('profile')


@login_required(login_url='/login/')
def program(request, program_id):
    """This function is used to show the details of a program."""

    program = get_object_or_404(Program, id=program_id) # getting program
    sessions = Session.objects.filter(program_id=program_id)
    sessions_dic = {}

    for session in sessions:
        exercices = Exercice.objects.filter(session_id=session.id)
        exercices = timedelta_no_hours(exercices)
        sessions_dic[session] = exercices

    context = {
        "program" : program,
        "sessions" : sessions_dic
    }

    return render(request, 'main/program.html', context)


def timedelta_no_hours(exercices):
    """Convert duration time in only minutes and seconds"""
    for exercice in exercices:
        time_in_seconds = exercice.cool.seconds
        minutes = time_in_seconds // 60
        seconds = time_in_seconds % 60
        if seconds == 0:
            seconds = "00"
        exercice.cool = f"{minutes}:{seconds}"
    return exercices
