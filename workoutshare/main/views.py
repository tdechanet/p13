"""This module is used to specify how a page is going to behave."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.forms.models import modelformset_factory

from .models import CustomUser, Program, Session, Exercice
from .forms import ExerciceForm

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
            return redirect('delete_program', program_id=program.id)

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

    if request.method == 'POST':

        # pointing to the right session
        session_id = request.POST.get('id')
        session = sessions[int(session_id)]

        return redirect('delete_session', session_id=session.id)

    context = {
        "program" : program,
        "sessions" : sessions_dic
    }

    return render(request, 'main/program.html', context)


def delete_session(request, session_id):
    """This function is used to permit a user to delete his sessions."""
    session = get_object_or_404(Session, id=session_id) # getting session
    program = session.program_id # getting program

    if program.user_id == request.user: # verifying that the session belong to the connected user
        session.delete()

    # redirect to the profile
    return redirect('program', program_id=program.id)


def session(request, session_id):
    """This function is used to permit a user to modify or create sessions."""
    session = get_object_or_404(Session, id=session_id) # getting session
    if session.get_owner() != request.user: # verifying that the session belong to the connected user 
        raise Http404()

    exercices = Exercice.objects.filter(session_id=session.pk)
    exercices = timedelta_no_hours(exercices)

    if request.method == 'POST':

        # pointing to the right program
        exercice_id = request.POST.get('id')
        exercice = exercices[int(exercice_id)]
        # redirect to delete url
        return redirect('delete_exercice', exercice_id=exercice.pk)
    
    ExerciceFormset = modelformset_factory(Exercice, form=ExerciceForm, extra=0)
    formset = ExerciceFormset(request.POST or None, queryset=exercices)
    if formset.is_valid():
        for form in formset:
            row = form.save(commit=False)
            if row.session_id == None:
                row.session_id = session.pk
            row.save()

    context = {
        "session" : session,
        "formset" : formset
    }

    return render(request, 'main/session.html', context)


def delete_exercice(request, exercice_id):
    """This function is used to permit a user to delete one of his exercices."""
    exercice = get_object_or_404(Exercice, id=exercice_id) # getting exercice
    session = exercice.session_id # getting session
    program = session.program_id # getting program
    
    if program.user_id == request.user: # verifying that the exercice belong to the connected user
        exercice.delete()

    # redirect to the session
    return redirect('session', session_id=session.id)


def new_exercice(request, session_id):
    """This function is used to permit a user to add a new exercice to a session."""
    session = get_object_or_404(Session, id=session_id) # getting session
    if session.get_owner() != request.user: # verifying that the session belong to the connected user 
        raise Http404()

    form = ExerciceForm(request.POST or None)

    if form.is_valid():
        row = form.save(commit=False)
        row.session_id = session
        row.save()
        
        return redirect('session', session_id=session.pk)

    context = {
        "session" : session,
        "form" : form
    }

    return render(request, 'main/new_exercice.html', context )


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
