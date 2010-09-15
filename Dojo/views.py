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
from forms import *

def club_list(request):

    info_dict = {
        'queryset':Club.objects.all(),
        'template_name':'Dojo/Club_object_list.html'
    }

    return list_detail.object_list(request, **info_dict)


def club_detail(request, club = None):

    info_dict = {
        'queryset':Club.objects.all(),
        'template_name':'Dojo/Club_object_detail.html',
        'slug':club,
        'slug_field':'Slug'
    }

    return list_detail.object_detail(request, **info_dict)

def practice_list(request, club = None):

    club = get_object_or_404(Club, Slug = club)
    practices = club.practice_set.all().annotate(NumPeople = Count('person'))

    return render_to_response('Dojo/Practice_object_list.html', locals(),
                              context_instance = RequestContext(request))




def practice_detail(request, id = None):
    pass

def person_list(request, club = None):
    if club:
        club_obj = Club.objects.get(Slug = club)
        active = club_obj.Members.filter(memberrecord__is_active = True).distinct()
        in_active = club_obj.Members.filter(memberrecord__is_active = False).distinct()
    else:
        club_obj = None
        active = Person.objects.filter(memberrecord__is_active = True).distinct()
        in_active = Person.objects.filter(memberrecord__is_active = False).distinct()

    active = active.annotate(PracticeNum = Count('practicerecord'))
    info_dict = {
        'active_members':active,
        'inactive_members':in_active,
        'club':club_obj
    }

    return render_to_response('Dojo/Person_object_list.html', info_dict,
                              context_instance = RequestContext(request))

def person_detail(request, id = None):

    person = get_object_or_404(Person, id = int(id))
    clubs = person.club_set.all()
    recent_rank = person.Rank.latest()

    ReqFormset = formset_factory(RequirementForm, extra = 5)

    if request.method == 'POST':
        formset = ReqFormset(request.POST)
        if formset.is_valid():
            for form in formset.forms:
                if form.cleaned_data:
                    req = RequirementRecord(Person = person,
                                            DateOccured = form.cleaned_data['Date'],
                                            Requirement = form.cleaned_data['Requirement'])
                    req.save()
    else:
        formset = ReqFormset()
        


    practice_count = person.PracticeAttended.count()
    recent_practices = person.PracticeAttended.filter(practicerecord__DateOccured__gte = recent_rank.DateOccured)

    require_records = []
    for club in clubs:
        for req in club.requirement_set.all():
            records = RequirementRecord.objects.filter(Requirement = req,
                                                       Person = person)
            if records.count():
                latest_req = records.latest()
            else:
                latest_req = None
            print records, latest_req
            require_records.append({
                                    'requirement':req,
                                    'latest':latest_req
                                   })



    return render_to_response('Dojo/Person_object_detail.html', locals(),
                              context_instance = RequestContext(request))
    
def requirement_detail(request, slug = None):
    pass

def requirement_list(request):
    pass