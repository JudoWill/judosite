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
                                            ('Competition', 'Competition')))
    color = forms.ChoiceField(choices = (('White', 'White'),
                                            ('Blue', 'Blue')))
    size = forms.IntegerField(max_value = 7, min_value = 1)
    date = forms.DateField()
    person = ModelChoiceField('student')
    gi = forms.ModelChoiceField(queryset = GiType.objects.all(),
                                required = False, widget = forms.HiddenInput)


    def clean(self):
        data = self.cleaned_data
        try:
            gi = GiType.objects.get(description = data['gi_type'],
                                    color = data['color'],
                                    weave = data['weave'],
                                    size = data['size'])
        except GiType.DoesNotExist:
            raise forms.ValidationError('No such gi!')
        except GiType.MultipleObjectsReturned:
            raise forms.ValidationError('Not specific enough!')
        data['gi'] = gi
        return data




class NewOrder(ModelForm):
    gitype = forms.ModelChoiceField(queryset = GiType.objects.all())
    person = ModelChoiceField('student')


    class Meta:
        model = GiOrder
        exclude = ('closed', )
        fields = ('paid', 'date', 'person')
