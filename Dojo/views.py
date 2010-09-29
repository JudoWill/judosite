# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Max
from django.views.generic import list_detail
from django.views.decorators.cache import cache_page, never_cache
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.core.urlresolvers import reverse
from csv import DictReader, DictWriter
from StringIO import StringIO
from copy import deepcopy
from operator import itemgetter
from collections import defaultdict
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from models import *
from forms import *

def club_list(request):

    info_dict = {
        'queryset':Club.objects.all(),
        'template_name':'Dojo/Club_object_list.html'
    }

    return list_detail.object_list(request, **info_dict)

def search(request):
    print request.DATA

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
    practices = club.practice_set.all().annotate(NumPeople = Count('person')).order_by('-Date')

    if request.method == 'POST':
        form = PracticeModelForm(request.POST)
        new_practice = form.save(commit = False)
        new_practice.Club = club
        new_practice.save()
        return HttpResponseRedirect(new_practice.get_absolute_url())
            
    else:
        form = PracticeModelForm()

    return render_to_response('Dojo/Practice_object_list.html', locals(),
                              context_instance = RequestContext(request))

@login_required
def practice_detail(request, club = None, id = None):

    club = get_object_or_404(Club, Slug = club)
    practice = Practice.objects.get(id = int(id))
    request.session['last_page'] = request.path
    if request.method == 'POST':
        form = PracticeForm(request.POST)
        if form.is_valid():
            person = form.cleaned_data.get('Person', None)
            if person is None:
                person = Person(Name = form.cleaned_data['New_person'])
                person.save()
                mr = MemberRecord(Person = person,
                                  Club = club,
                                  DateOccured = practice.Date)
                mr.save()
                rr = RankRecord(Rank = 'White', Person = person, DateOccured = practice.Date)
                rr.save()
                messages.success(request, '%s was added succeessfuly to %s as a White belt.' % (person.Name, club.Name))

            pr, new_r = PracticeRecord.objects.get_or_create(Practice = practice,
                                                         DateOccured = practice.Date,
                                                         Person = person)
               
            if new_r:
                messages.success(request, '%s was added succeessfuly to this practice.' % person.Name)

            return HttpResponseRedirect(practice.get_absolute_url())


    else:
        form = PracticeForm()
        print 'made in get'



    info_dict = {
        'form':form,
        'club':club,
        'practice':practice
    }
    print info_dict
    return render_to_response('Dojo/Practice_object_detail.html', info_dict,
                              context_instance = RequestContext(request))

def person_list(request, club = None):
    if club:
        club_obj = Club.objects.get(Slug = club)
        players = club_obj.Members.annotate(last_practice = Max('practicerecord__DateOccured'))
    else:
        club_obj = None
        players = Person.objects.all().annotate(last_practice = Max('practicerecord__DateOccured'))


    request.session['last_page'] = request.path
    players = players.annotate(PracticeNum = Count('practicerecord'))
    info_dict = {
        'players':players,
        'club':club_obj
    }

    return render_to_response('Dojo/Person_object_list.html', info_dict,
                              context_instance = RequestContext(request))
@login_required
def person_detail(request, id = None):

    person = get_object_or_404(Person, id = int(id))
    clubs = person.club_set.all()
    try:
        recent_rank = person.rankrecord_set.latest()
    except ObjectDoesNotExist:
        recent_rank = None

    ReqFormset = formset_factory(RequirementForm, extra = 5)
    RankFormset = inlineformset_factory(Person, RankRecord, extra = 5)

    if request.method == 'POST':
        formset = ReqFormset(request.POST, prefix = 'req')
        PersonInfo = PersonInfoForm(request.POST, prefix = 'info', 
                                        instance = person)
        rank_formset = RankFormset(request.POST, instance = person, prefix = 'rank')
        
        if formset.is_valid() and PersonInfo.is_valid() and rank_formset.is_valid():
            for form in formset.forms:
                if form.cleaned_data:
                    req = RequirementRecord(Person = person,
                                            DateOccured = form.cleaned_data['Date'],
                                            Requirement = form.cleaned_data['Requirement'])
                    req.save()
                    messages.success(request, '%s was added succeessfuly for %s.' % (req.Requirement, person.Name))
            if PersonInfo.is_valid():
                new_p = PersonInfo.save(commit = False)
                if new_p.Email != person.Email:
                    messages.success(request, '%s was added succeessfuly for %s.' % ('Email', person.Name))
                if new_p.Name != person.Name:
                    messages.success(request, '%s was added succeessfuly for %s.' % ('Name', person.Name))
                new_p.save()
            if rank_formset.is_valid():
                t = rank_formset.save(commit = False)
                if t:
                    for rank in t:
                        rank.save()
                    messages.success(request, '%s was added succeessfuly for %s.' % ('Rank', person.Name))

                return HttpResponseRedirect(request.session.get('last_page', reverse('person_list')))
    else:
        formset = ReqFormset(prefix = 'req')
        PersonInfo = PersonInfoForm(instance = person, prefix = 'info')
        rank_formset = RankFormset(instance = person, prefix = 'rank')
        


    practice_count = person.PracticeAttended.count()
    if recent_rank is not None:
        recent_practices = person.PracticeAttended.filter(practicerecord__DateOccured__gte = recent_rank.DateOccured)
    else:
        recent_practices = person.PracticeAttended.all()
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