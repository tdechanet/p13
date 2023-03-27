"""This module is used to create forms that we can use in the app."""
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field
from django.forms import ModelForm #pylint: disable=E0401
from main.models import Exercice, Session, Program #pylint: disable=E0401


class ExerciceForm(ModelForm):
    """This class is used to define the exercice form"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Exercice
        fields = ['id', 'name', 'muscle_group_id', 'sets', 'reps', 'cool']


class SessionForm(ModelForm):
    """This class is used to define the session form"""
    class Meta:
        model = Session
        fields = ['name']
        labels = {"name": ""}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('name', id="session_form", data_name="new_session")
        )

class ProgramForm(ModelForm):
    """This class is used to define the program form"""
    class Meta:
        model = Program
        fields = ['name']
        labels = {"name": ""}
