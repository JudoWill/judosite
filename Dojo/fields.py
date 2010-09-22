from django import forms
from django.conf import settings
from django.db.models.query_utils import Q
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from models import *
from autocomplete.fields import ModelChoiceField

class StudentChoiceField(ModelChoiceField):

    pass

