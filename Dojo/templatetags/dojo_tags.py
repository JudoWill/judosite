from Dojo.models import *
from django import template
from Dojo.utils import get_missing_reqs
from datetime import timedelta, date
register = template.Library()


@register.simple_tag
def num_classes_by_club(student, club):
    qset = PracticeRecord.objects.filter(Person = student)
    if club:
        qset = qset.filter(Practice__Club = club)
    return qset.count()
                                        
@register.inclusion_tag('Dojo/requirement_list_short.html')
def missing_reqs_by_club(student, club):
    missing = []
    for req in club.requirement_set.all():
        last_date = date.today() - timedelta(req.Valid_for)
        qset = student.requirementrecord_set.filter(DateOccured__gte = last_date,
                                                   Requirement = req)
        if not qset.exists():
            missing.append(req.id)
    
    return {'requirements':Requirement.objects.filter(id__in = missing)}

@register.inclusion_tag('Dojo/person_list_active_short.html')
def list_active_players(qset, club):
    return {'person_list':qset, 'club':club}
    
@register.inclusion_tag('Dojo/person_list_inactive_short.html')
def list_inactive_players(qset, club):
    return {'person_list':qset, 'club':club}