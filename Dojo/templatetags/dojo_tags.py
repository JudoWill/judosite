from Dojo.models import *
from django import template
from Dojo.utils import get_missing_reqs
from datetime import timedelta
register = template.Library()


@register.simple_tag
def num_classes_by_club(student, club):
    return PracticeRecord.objects.filter(Person = student, 
                                        Practice__Club = club).count()
                                        
@register.simple_tag
def missing_reqs_by_club(student, club):
    missing = []
    for req in club.requirement_set.all():
        last_date = date_check - timedelta(req.Valid_for)
        qset = student.requirementrecord_set.filter(DateOccured__gte = last_date,
                                                   Requirement = req)
        if not qset.exists():
            missing.append(req)
    
    return Requirement.objects.filter(id__in = missing)
    