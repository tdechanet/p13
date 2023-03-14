from crispy_forms.helper import FormHelper
from django.forms import ModelForm
from main.models import Exercice, Session


class ExerciceForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExerciceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = Exercice
        fields = ['id', 'name', 'muscle_group_id', 'sets', 'reps', 'cool']


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ['name']
        labels = {"name": ""}
