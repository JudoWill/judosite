from django.forms import ModelForm
from django import forms
from models import *




class RequirementForm(forms.Form):
    Requirement = forms.ModelChoiceField(queryset = Requirement.objects.all())
    Date = forms.DateField()

