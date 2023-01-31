"""This module is used to specify forms and use them in views."""
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    """This class is used to configure the registering forms."""
    email = forms.EmailField(required=True)

    class Meta: #pylint: disable=R0903
        """This class is used to specify the model and the fields that the form is using."""
        model = User
        fields = ('username', 'email', 'password1', 'password2')
