from django import forms
from .models import Objective,KeyResult, MonthResult, Action
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper


class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ['brand', 'team', 'year', 'goal']
        widgets = {
            'goal': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # Crispy negeneruoja <form> tago

class KeyResultForm(forms.ModelForm):
    class Meta:
        model = KeyResult
        fields = ['name', 'unit', 'annual_goal', 'distribution_type']
        widgets = {
            'name': forms.TextInput(attrs={'list': 'kr-suggestions'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False  # Crispy negeneruoja <form> tago

class MonthResultForm(forms.ModelForm):
    class Meta:
        model = MonthResult
        fields = ['actual_result']

class ActionForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['action_item', 'unit', 'planned_result', 'actual_result', 'is_done', 'notes']

class ActionUpdateForm(forms.ModelForm):
    class Meta:
        model = Action
        fields = ['actual_result', 'is_done', 'notes']

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']