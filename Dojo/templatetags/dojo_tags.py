from Dojo.models import *
from django import template
from Dojo.utils import get_missing_reqs
from datetime import timedelta, date
from Dojo.forms import *
import re
register = template.Library()


@register.simple_tag
def num_classes_by_club(student, club):
    qset = PracticeRecord.objects.filter(Person = student)
    try:
        qset = qset.filter(Practice__Club = club)
    except ValueError:
        pass
    return qset.count()

@register.inclusion_tag('Dojo/requirement_list_short.html')
def missing_reqs_by_club(student, club):
    missing = []
    try:
        reqs = club.requirement_set.all()
    except AttributeError:
        reqs = Requirement.objects.filter(Club__in = student.club_set.all())
    for req in reqs:
        last_date = date.today() - timedelta(req.Valid_for)
        qset = student.requirementrecord_set.filter(DateOccured__gte = last_date,
                                                   Requirement = req)
        if not qset.exists():
            missing.append(req.id)
    
    return {'requirements':Requirement.objects.filter(id__in = missing)}

@register.inclusion_tag('Dojo/person_list_active_short.html')
def list_active_players(club):
    if club == 'None':
        club = None
    qset = Person.objects.club_qset(club)

    return {'person_list':qset, 'club':club}
    
@register.inclusion_tag('Dojo/person_list_inactive_short.html')
def list_inactive_players(club):
    if club == 'None':
        club = None
    qset = Person.objects.club_qset(club).order_by('-last_practice')

    return {'person_list':qset, 'club':club}
    
@register.inclusion_tag('Dojo/practice_form.html')
def practice_form():
    
    practice_form = LPracticeForm()
    
    return {'practice_form':practice_form}
    