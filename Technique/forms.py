from django.forms import ModelForm
from django import forms
from models import *


class TechniqueForm(ModelForm):
    
    class Meta:
        model = Technique

        
class TechniqueTagForm(ModelForm):
    
    class Meta:
        model = TechniqueTag