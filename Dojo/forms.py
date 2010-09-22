from django.forms import ModelForm
from django import forms
from models import *

from autocomplete import ModelChoiceField


class RequirementForm(forms.Form):
    Requirement = forms.ModelChoiceField(queryset = Requirement.objects.all())
    Date = forms.DateField()

class PracticeForm(forms.Form):
    Students = ModelChoiceField('student')


class PracticeModelForm(ModelForm):
    class Meta:
        model = Practice
        exclude = ('Club',)
    