from django.forms import ModelForm
from django import forms
from models import *
from fields import LocalModelChoiceField
from autocomplete.fields import ModelChoiceField
from django.contrib.admin.widgets import AdminDateWidget


class RequirementForm(forms.Form):
    Requirement = forms.ModelChoiceField(queryset = Requirement.objects.all())
    Date = forms.DateField()

class PersonInfoForm(ModelForm):
    class Meta:
        model = Person
        fields = ['Name', 'Email', 'is_instructor', 'Picture', 'Gender']
        

class PracticeForm(forms.Form):
    Person = LocalModelChoiceField('student', required = False)
    New_person = forms.CharField(required = False)
    Technique = LocalModelChoiceField('technique', required = False)
    New_technique = forms.CharField(required = False)
    

    def clean(self):
        
        if not any(self.cleaned_data.values()):
            raise forms.ValidationError('You must have at least 1 field!')
            
        return self.cleaned_data

        

class PracticeModelForm(ModelForm):
    Date = forms.DateField(widget = AdminDateWidget)
    class Meta:
        model = Practice
        exclude = ('Club',)
    