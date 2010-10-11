from django.forms import ModelForm
from django import forms
from models import *


class TechniqueForm(ModelForm):
    
    class Meta:
        model = Technique
        exclude = ['Practices']

        
class TechniqueTagForm(ModelForm):
    
    class Meta:
        model = TechniqueTag