from django import forms
from django.conf import settings
from django.db.models.query_utils import Q
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from models import *

class StudentMultipleChoice(forms.CharField):

    class Media:
        js = (
            settings.MEDIA_URL+'/'+'development-bundle/jquery-1.4.2.js',
            settings.MEDIA_URL+'/'+'development-bundle/ui/jquery.ui.autocomplete.js',
        )
        

    def __init__(self, *args, **kwargs):
        super(StudentMultipleChoice, self).__init__(*args, **kwargs)

    def to_python(self, value):

        if not value:
            return None

        new_ids = []
        old_ids = []
        names = map(lambda x: x.strip(), value.split(';'))
        for name in names:
            if len(name):
                person,isnew = Person.objects.get_or_create(Name = name)
                if isnew:
                    new_ids.append(person.id)
                else:
                    old_ids.append(person.id)
        new_qset = Person.objects.filter(pk__in = new_ids)
        old_qset = Person.objects.filter(pk__in = old_ids)
        return new_qset, old_qset

    def validate(self, value):
        pass


