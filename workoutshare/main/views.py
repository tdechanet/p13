"""This module is used to specify how a page is going to behave."""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.forms.models import modelformset_factory
from django.utils import timezone

from authentication.models import Following #pylint: disable=E0401
from .models import CustomUser, Program, Session, Exercice, Favorite
from .forms import ExerciceForm, SessionForm, ProgramForm

# Create your views here.


@login_required(login_url='/login/')
def home_page(request):
    """This function is used to show to a user all the programs he follows."""

    #getting the posted programs of the followed users
    programs = Program.objects.filter(
        user_id__authors__follower=request.user,
        published=1).order_by('-updated_at')

    context = {
        "programs" : programs
    }

    return render (request, 'main/home.html', context)


def legal_mention(request):
    """This function is used to show the legal-mention page."""

    return render (request, 'legal_mention.html')


@login_required(login_url='/login/')
def favorite_page(request):
    """This fuction is used to show to a user his favorites programs."""

    #getting the favorites programs of the user
    favorites = Program.objects.filter(favorite__user_id=request.user)

    #user want to unfavorite a program
    if request.method == 'POST':
        # pointing to the right program
        program_id = request.POST.get('id')
        program_selected = favorites[int(program_id)]
        favorite_selected = Favorite.objects.get(program_id=program_selected)
        favorite_selected.delete()

    context = {
        "favorites" : favorites
    }

    return render(request, 'main/favorite.html', context)


@login_required(login_url='/login/')
def profile_page(request, user_id=None): #pylint: disable=R0914, disable=R0912
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

        # we also check if some of the programs are his favorites
        for program in programs:
            try:
                program.favorites = Favorite.objects.get(program_id=program, user_id=request.user)
            except Favorite.DoesNotExist:
                program.favorites = False

    new_program_form = ProgramForm(request.POST or None)

    if request.method == 'POST':
        
        # if the user want to create a program we ask the name of the program
        if 'new_program' in request.POST:
            if is_owner:
                if new_program_form.is_valid():
                    new_program_form_raw = new_program_form.save(commit=False)
                    new_program_form_raw.user_id = request.user
                    new_program_form_raw.save()

                    #redirect to the new program page
                    return redirect('program', program_id=new_program_form_raw.id)

        elif 'user_follow' in request.POST:
            # reverse following state

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
                if is_owner:
                    # reverse published state
                    program_selected.published = not program_selected.published
                    program_selected.save()

            if 'program_favorite' in request.POST:
                # reverse favorite state
                if program_selected.favorites:
                    program_selected.favorites.delete()
                else:
                    new_favorite = Favorite(program_id=program_selected, user_id=request.user)
                    new_favorite.save()

            # redirect to delete url
            if 'program_delete' in request.POST:
                return redirect('delete_program', program_id=program_selected.pk)

        # we redirect to same page to actualize potential changes
        return redirect('profile', user_id=selected_user_id)

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
        "program_form" : new_program_form,
    }

    return render(request, 'main/profile.html', context)


def delete_program_page(request, program_id):
    """This function is used to permit a user to delete his programs."""
    program_selected = get_object_or_404(Program, id=program_id) # getting program
    # verifying that the program belong to the connected user
    if program_selected.user_id == request.user:
        program_selected.delete()

    # redirect to the profile
    return redirect('profile')


@login_required(login_url='/login/')
def program_page(request, program_id):
    """This function is used to show the details of a program."""

    program_selected = get_object_or_404(Program, id=program_id) # getting program
    program_selected_name = program_selected.name

    sessions = Session.objects.filter(program_id=program_id) # getting the sessions in the program

    # checking if the user is the owner of the program
    is_owner = request.user == program_selected.user_id

    #creating form in case user want to create a new session
    new_session_form = SessionForm(request.POST or None)

    #this form is used to let the user modify the name of the program
    modify_program_name_form = ProgramForm(request.POST or None, instance=program_selected)

    if request.method == 'POST':
        
        # we actualize the updated at of the program_selected
        program_selected.updated_at = timezone.now()
        program_selected.save()

        if 'session_delete' in request.POST:
            # pointing to the right session
            session_id = request.POST.get('id')
            session = sessions[int(session_id)]
            return redirect('delete_session', session_id=session.pk)

        # we create the new session and redirect to the new session page
        if 'new_session' in request.POST:
            if is_owner:
                if new_session_form.is_valid():
                    new_session_form_raw = new_session_form.save(commit=False)
                    new_session_form_raw.program_id = program_selected
                    new_session_form_raw.save()
                    return redirect('session', session_id=new_session_form_raw.id)

        #the user want to modify the name of the program
        if 'modify_program_name' in request.POST:
            if is_owner:
                if modify_program_name_form.is_valid():
                    modify_program_name_form.save()
                    return redirect('program', program_id=program_selected.pk)

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
        "session_form" : new_session_form,
        "program_name_form" : modify_program_name_form
    }

    return render(request, 'main/program.html', context)


def delete_session_page(request, session_id):
    """This function is used to permit a user to delete his sessions."""
    session = get_object_or_404(Session, id=session_id) # getting session

    program_selected = Program.objects.get(id=session.program_id.pk) # getting program
    # verifying that the session belong to the connected user
    if program_selected.user_id == request.user:
        session.delete()

    # redirect to the profile
    return redirect('program', program_id=program_selected.pk)


@login_required(login_url='/login/')
def session_page(request, session_id):
    """This function is used to permit a user to modify or create sessions."""
    session = get_object_or_404(Session, id=session_id) # getting session
    if session.get_owner() != request.user: #verifying that the session belong to the connected user
        raise Http404()

    #getting the exercice linked to the session and clean the time data
    exercices = Exercice.objects.filter(session_id=session.pk)
    exercices = timedelta_no_hours(exercices)

    #create the formset of the exercices
    exercice_formset = modelformset_factory(Exercice, form=ExerciceForm, extra=0)
    formset = exercice_formset(request.POST or None, queryset=exercices)

    #create the form that let the user modify the name of the session
    session_name_form = SessionForm(request.POST or None, instance=session)

    if request.method == 'POST':

        #we update the program updated at field
        session_program = session.program_id
        session_program.updated_at = timezone.now()
        session_program.save()

        if 'exercice_delete' in request.POST:
            # pointing to the right program
            exercice_id = request.POST.get('id')
            exercice = exercices[int(exercice_id)]
            # redirect to delete url
            return redirect('delete_exercice', exercice_id=exercice.pk)

        #we verify that the form for the exercices are correct and the form of session name
        if 'save_session' in request.POST:
            if formset.is_valid() and session_name_form.is_valid():
                for form in formset:
                    row = form.save(commit=False)
                    row.save()
                    session_name_form.save()
                return redirect('program', program_id = session.program_id.pk)

    context = {
        "session" : session,
        "formset" : formset,
        "session_form" : session_name_form
    }

    return render(request, 'main/session.html', context)


def delete_exercice_page(request, exercice_id):
    """This function is used to permit a user to delete one of his exercices."""
    exercice = get_object_or_404(Exercice, id=exercice_id) # getting exercice
    session = exercice.session_id # getting session
    program = session.program_id # getting program

    if program.user_id == request.user: # verifying that the exercice belong to the connected user
        exercice.delete()

    # redirect to the session
    return redirect('session', session_id=session.id)


def new_exercice_page(request, session_id):
    """This function is used to permit a user to add a new exercice to a session."""
    session = get_object_or_404(Session, id=session_id) # getting session
    if session.get_owner() != request.user: #verifying that the session belong to the connected user
        raise Http404()

    form = ExerciceForm(request.POST or None)

    if form.is_valid():
        row = form.save(commit=False)
        row.session_id = session
        row.save()

        # we update the program update at field
        session_program = session.program_id
        session_program.updated_at = timezone.now()
        session_program.save()

        #redirect to the linked session
        return redirect('session', session_id=session.pk)

    context = {
        "session" : session,
        "form" : form
    }

    return render(request, 'main/new_exercice.html', context )


@login_required(login_url='/login/')
def user_research_page(request):
    """This method permit the user to research other users."""

    # using trigarm reserach for user reserach
    query = request.GET.get("user_research_bar")
    research_results = CustomUser.objects.filter(username__trigram_similar=query)

    users_details = []

    # building the lost of potential corresponding users
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
