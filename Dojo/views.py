# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import list_detail
from django.views.decorators.cache import cache_page, never_cache
from django.http import HttpResponse, HttpResponseRedirect
from csv import DictReader, DictWriter
from StringIO import StringIO
from copy import deepcopy
from operator import itemgetter
from collections import defaultdict

from models import *

def club_list(request):

    info_dict = {
        'queryset':Club.objects.all(),
        'template_name':'Club/object_list.html'
    }

    return list_detail.object_list(request, **info_dict)


def club_detail(request, club = None):
    pass

def practice_list(request, club = None):
    pass

def practice_detail(request, club = None, id = None):
    pass

def person_list(request, club = None):
    pass

def person_detail(request, club = None, id = None):
    pass