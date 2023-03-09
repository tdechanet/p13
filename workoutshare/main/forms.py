from django.forms import ModelForm
from main.models import Exercice


class ExerciceForm(ModelForm):
    class Meta:
        model = Exercice
        fields = ['id', 'name', 'muscle_group_id', 'sets', 'reps', 'cool']
