from django.forms import ModelForm
from django import forms
from models import *
from autocomplete.fields import ModelChoiceField


class TechniqueForm(ModelForm):
    
    class Meta:
        model = Technique
        exclude = ['Practices']

        
class TechniqueTagForm(ModelForm):
    
    class Meta:
        model = TechniqueTag
        exclude = ['Technique']

class AddTechForm(forms.Form):
    New_Technique = forms.CharField(required = False)
    Technique = ModelChoiceField('technique', required = False)

    def clean(self):

        np, op = self.cleaned_data['New_Technique'], self.cleaned_data['Technique']
        if np is None and op is None:
            raise forms.ValidationError('You must specify either New Technique or Old Technique!')

        return self.cleaned_data

class AddTagForm(forms.Form):
    New_Tag = forms.CharField(required = False)
    Tag = ModelChoiceField('techniquetag', required = False)

    def clean(self):

        np, op = self.cleaned_data['New_Tag'], self.cleaned_data['Tag']
        if np is None and op is None:
            raise forms.ValidationError('You must specify either New Technique or Old Technique!')

        return self.cleaned_data