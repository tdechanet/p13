"""This module is used to specify how a page is going to behave."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Program, Session, Exercice

# Create your views here.

@login_required(login_url='/login/')
def profile(request):
    """This function is used to show to a user all his programs."""

    # getting the programs of the user
    programs = Program.objects.filter(user_id=request.user.pk).order_by('name')

    if request.method == 'POST':

        # pointing to the right program
        program_id = request.POST.get('id')
        program_selected = programs[int(program_id)]

        if 'program_publish' in request.POST:

            # reverse published state
            program_selected.published = not program_selected.published
            program_selected.save()

        # redirect to delete url
        if 'program_delete' in request.POST:
            return redirect('delete_program', program_id=program_selected.pk)


    # getting the number of followers of the user
    number_of_followers = CustomUser.objects.filter(authors=request.user.pk).count()

    context = {
        "followers": number_of_followers,
        "programs": programs,
    }

    return render(request, 'main/profile.html', context)


def delete_program(request, program_id):
    """This function is used to permit a user to delete his programs."""
    program_selected = get_object_or_404(Program, id=program_id) # getting program
    # verifying that the program belong to the connected user
    if program_selected.user_id == request.user:
        program_selected.delete()

    # redirect to the profile
    return redirect('profile')


@login_required(login_url='/login/')
def program(request, program_id):
    """This function is used to show the details of a program."""

    program_selected = get_object_or_404(Program, id=program_id) # getting program
    program_selected_name = program_selected.name

    sessions = Session.objects.filter(program_id=program_id) # getting the sessions in the program

    if request.method == 'POST':

        # pointing to the right session
        session_id = request.POST.get('id')
        session = sessions[int(session_id)]

        return redirect('delete_session', session_id=session.pk)

    # building a dict of exercices for each sessions
    sessions_dic = {}
    for session in sessions:
        exercices = Exercice.objects.filter(session_id=session.pk)
        exercices_fixed_time = timedelta_no_hours(exercices)
        sessions_dic[session.name] = exercices_fixed_time

    context = {
        "program" : program_selected_name,
        "sessions" : sessions_dic
    }

    return render(request, 'main/program.html', context)


def delete_session(request, session_id):
    """This function is used to permit a user to delete his sessions."""
    session = get_object_or_404(Session, id=session_id) # getting session
    program_selected = Program.objects.get(id=session.program_id.pk) # getting program
    # verifying that the session belong to the connected user
    if program_selected.user_id == request.user:
        session.delete()

    # redirect to the profile
    return redirect('program', program_id=program_selected.pk)

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
