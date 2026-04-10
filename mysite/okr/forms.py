from django import forms
from .models import Objective,KeyResult, MonthResult, Action

class ObjectiveForm(forms.ModelForm):
    class Meta:
        model = Objective
        fields = ['brand', 'team', 'year', 'goal']
        widgets = {
            'goal': forms.Textarea(attrs={'rows': 3}),
        }

class KeyResultForm(forms.ModelForm):
    class Meta:
        model = KeyResult
        fields = ['name', 'unit', 'annual_goal', 'distribution_type']
        widgets = {
            'name': forms.TextInput(attrs={'list': 'kr-suggestions'}),
        }

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