"""This module is used to specify how a page is going to behave."""
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from .models import CustomUser, Program

# Create your views here.

@login_required(login_url='/login/')
def profile(request):
    """This function is used to show to a user all his programs."""

    # getting the number of followers of the user
    number_of_followers = CustomUser.objects.filter(authors=request.user.id).count()

    # getting the programs of the user
    programs = Program.objects.filter(user_id=request.user.id).order_by('name')

    if request.method == 'POST':
        program_id = request.POST.get('id')
        program = programs[int(program_id)]

        if 'program_publish' in request.POST:
            form = request.POST.get('program_publish')

            if form == "True":
                program.published = False
            else:
                program.published = True

            program.save()

        if 'program_delete' in request.POST:
            return HttpResponseRedirect(f'{program.id}/delete/')


    context = {
        "followers": number_of_followers,
        "programs": programs,
    }

    return render(request, 'main/profile.html', context)


def delete_program(request, program_id):
    """This function is used to permit a user to delete his programs."""
    program =  get_object_or_404(Program, id=program_id)

    if program.user_id == request.user:
        program.delete()

    return redirect('profile')
