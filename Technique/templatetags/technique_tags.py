from Dojo.models import *
from Technique.models import *
from django import template
from Dojo.utils import get_missing_reqs
from datetime import timedelta, date
import re
register = template.Library()


@register.influsion_tag('Technique/Technique_list_short.html')
def list_techniques():
    pass