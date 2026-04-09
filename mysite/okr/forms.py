from django import forms
from .models import Objective,KeyResult

class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ['brand', 'team', 'year', 'goal']

class KeyResultForm(forms.ModelForm):
    class Meta:
        model = KeyResult
        fields = ['name', 'unit', 'annual_goal', 'distribution_type']


