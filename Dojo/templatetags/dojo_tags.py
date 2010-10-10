from Dojo.models import *
from django import template

register = template.Library()


@register.simple_tag
def num_classes_by_club(student, club):
    return PracticeRecord.objects.filter(Person = student, 
                                        Practice__Club = club).count()