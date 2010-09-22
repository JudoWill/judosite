from django.forms import ModelForm
from django import forms
from models import *
from fields import StudentChoiceField
from django.contrib.admin.widgets import AdminDateWidget


class RequirementForm(forms.Form):
    Requirement = forms.ModelChoiceField(queryset = Requirement.objects.all())
    Date = forms.DateField()

class PersonInfoForm(ModelForm):
    class Meta:
        model = Person
        include = ['Name', 'Email', 'is_instructor', 'Picture']
        

class PracticeForm(forms.Form):
    New_person = forms.CharField(required = False)
    Person = StudentChoiceField('student', required = False)

    def clean(self):

        np, op = self.cleaned_data['New_person'], self.cleaned_data['Person']
        if np is None and op is None:
            raise forms.ValidationError('You must specify either New Person or Old Person!')

        return self.cleaned_data

        

class PracticeModelForm(ModelForm):
    Date = forms.DateField(widget = AdminDateWidget)
    class Meta:
        model = Practice
        exclude = ('Club',)
    