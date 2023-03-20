"""This module is used to specify how a page is going to behave."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.forms.models import modelformset_factory

from authentication.models import Following #pylint: disable=E0401
from .models import CustomUser, Program, Session, Exercice
from .forms import ExerciceForm, SessionForm, ProgramForm

# Create your views here.


@login_required(login_url='/login/')
def home(request):
    """This function is used to show to a user all the programs he follows."""

    programs = Program.objects.filter(user_id__authors__follower=request.user, published=1).order_by('-updated_at')

    context = {
        "programs" : programs
    }

    return render (request, 'main/home.html', context)


def legal_mention(request):
    """This function is used to show the legal-mention page."""

    return render (request, 'legal_mention.html')


@login_required(login_url='/login/')
def profile(request, user_id=None):
    """This function is used to show to a user all his programs."""

    # if a user id as been specified in the url we use it, else we use the id of the connected user
    selected_user_id = user_id if user_id else request.user.pk
    selected_user = CustomUser.objects.get(pk=selected_user_id)

    # getting the programs of the user
    programs = Program.objects.filter(user_id=selected_user).order_by('name')

    # checking if the user is the owner of the profile
    is_owner = request.user == selected_user

    # if the connected user is not the owner of the profile we check if he is a follower
    is_following = False
    if not is_owner:
        try:
            follow_row = Following.objects.get(author=selected_user, follower=request.user)
            is_following = True
        except Following.DoesNotExist:
            follow_row = None

    new_program_form = ProgramForm(request.POST or None)

    if request.method == 'POST':
    
        if 'new_program' in request.POST:
            if is_owner:
                if new_program_form.is_valid():
                    new_program_form_raw = new_program_form.save(commit=False)
                    new_program_form_raw.user_id = request.user
                    new_program_form_raw.save()
                    return redirect('program', program_id=new_program_form_raw.id)

        if 'user_follow' in request.POST:
            # reverse following state
            is_following = not is_following

            if follow_row:
                follow_row.delete()

            else:
                follow_row = Following(author=selected_user, follower=request.user)
                follow_row.save()
        
        else:
            
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

    followers = []

    # getting the number of followers of the user
    follow_row = Following.objects.filter(author=selected_user)
    for link in follow_row:
        followers.append(link.follower)


    # getting the username of the profile owner
    username = selected_user.username

    context = {
        "followers": followers,
        "programs": programs,
        "is_owner" : is_owner,
        "is_following" : is_following,
        "username" : username,
        "program_form" : new_program_form
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

    # checking if the user is the owner of the program
    is_owner = request.user == program_selected.user_id

    new_session_form = SessionForm(request.POST or None)

    if request.method == 'POST':

        if 'session_delete' in request.POST:
            # pointing to the right session
            session_id = request.POST.get('id')
            session = sessions[int(session_id)]
            return redirect('delete_session', session_id=session.pk)
    
        if 'new_session' in request.POST:
            if is_owner:
                if new_session_form.is_valid():
                    new_session_form_raw = new_session_form.save(commit=False)
                    new_session_form_raw.program_id = program_selected
                    new_session_form_raw.save()
                    return redirect('session', session_id=new_session_form_raw.id)

    # building a dict of exercices for each sessions
    sessions_list = []
    for session in sessions:
        exercices = Exercice.objects.filter(session_id=session.pk)
        exercices_fixed_time = timedelta_no_hours(exercices)
        sessions_list.append((session, exercices_fixed_time))

    context = {
        "program_name" : program_selected_name,
        "sessions_list" : sessions_list,
        "is_owner" : is_owner,
        "session_form" : new_session_form
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


def create_session(request, program_pk, session_name):
    program_selected = get_object_or_404(Program, id=program_pk) # getting program
    # verifying that the program belong to the connected user
    if program_selected.user_id == request.user:
        new_session = Session(program_id=program_pk, name=session_name)
        new_session.save()

    else:
        return redirect('profile')

    return redirect('new_exercice', session_id=new_session.pk)


@login_required(login_url='/login/')
def session(request, session_id):
    """This function is used to permit a user to modify or create sessions."""
    session = get_object_or_404(Session, id=session_id) # getting session
    if session.get_owner() != request.user: # verifying that the session belong to the connected user 
        raise Http404()

    exercices = Exercice.objects.filter(session_id=session.pk)
    exercices = timedelta_no_hours(exercices)

    ExerciceFormset = modelformset_factory(Exercice, form=ExerciceForm, extra=0)
    formset = ExerciceFormset(request.POST or None, queryset=exercices)

    session_name_form = SessionForm(request.POST or None, instance=session)

    if request.method == 'POST':

        if 'exercice_delete' in request.POST:
            # pointing to the right program
            exercice_id = request.POST.get('id')
            exercice = exercices[int(exercice_id)]
            # redirect to delete url
            return redirect('delete_exercice', exercice_id=exercice.pk)
        
        if 'save_session' in request.POST:
            if formset.is_valid() and session_name_form.is_valid():
                for form in formset:
                    row = form.save(commit=False)
                    if row.session_id == None:
                        row.session_id = session.pk
                    row.save()
                    session_name_form.save()
                return redirect('program', program_id = session.program_id.pk)

    context = {
        "session" : session,
        "formset" : formset,
        "session_form" : session_name_form
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


@login_required(login_url='/login/')
def user_research(request):
    query = request.GET.get("user_research_bar")
    research_results = CustomUser.objects.filter(username__trigram_similar=query)

    users_details = []

    for user in research_results:
        programs = Program.objects.filter(user_id=user)
        users_details.append((user, programs.count()))

    context = {
        "users_details" : users_details
    }

    return render(request, 'main/research_page.html', context)


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
