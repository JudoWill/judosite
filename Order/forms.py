from django.forms import ModelForm
from django import forms
from autocomplete.fields import ModelChoiceField
from models import *

class OrderStatusForm(ModelForm):
    
    class Meta:
        model = OrderStatus

class NOrder(forms.Form):
    gi_type = forms.ChoiceField(choices = (('Fuji', 'Fuji'),
                                            ('Mizuno', 'Mizuno')))
    weave = forms.ChoiceField(choices = (('Single', 'Single'),
                                            ('Double', 'Double'),
                                            ('Competition', 'Competition'))
    size = forms.IntegerField(max_value = 7, min_value = 1)
    order_date = forms.DateField()
    person = ModelChoiceField('student')



class NewOrder(ModelForm):
    gitype = forms.ModelChoiceField(queryset = GiType.objects.all())
    person = ModelChoiceField('student')


    class Meta:
        model = GiOrder
        exclude = ('closed', )
        fields = ('paid', 'date', 'person')
