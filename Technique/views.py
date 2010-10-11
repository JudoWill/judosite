# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Count, Max
from django.views.generic import list_detail

from Dojo.models import *
from Technique.models import *


def technique_list(request):

    info_dict = {
        'queryset':Technique.objects.all(),
        'template_name':'Technique/Technique_object_list.html'
    }

    return list_detail.object_list(request, **info_dict)

def technique_detail(request, technique = None):
    pass