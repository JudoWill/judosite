from django.forms import ModelForm
from django import forms
from autocomplete.fields import ModelChoiceField
from models import *

class OrderStatusForm(ModelForm):
    
    class Meta:
        model = OrderStatus

class NewOrder(ModelForm):
    gitype = forms.ModelChoiceField(queryset = GiType.objects.all())
    person = ModelChoiceField('student')


    class Meta:
        model = GiOrder
        exclude = ('closed', )
        fields = ('gitype', 'paid', 'date', 'person')
