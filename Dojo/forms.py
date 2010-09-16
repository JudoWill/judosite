from django.forms import ModelForm
from django import forms
from models import *

from fields import StudentMultipleChoice


class RequirementForm(forms.Form):
    Requirement = forms.ModelChoiceField(queryset = Requirement.objects.all())
    Date = forms.DateField()

class PracticeForm(forms.Form):
    Students = StudentMultipleChoice()


class PracticeModelForm(ModelForm):
    class Meta:
        model = Practice
        exclude = ('Club',)
    