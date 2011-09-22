# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory, modelformset_factory
from django.template import RequestContext
from django.views.generic import list_detail
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages

from Dojo.models import Club, Person, Practice
from Dojo.models import RequirementRecord, PracticeRecord, MemberRecord, RankRecord
from Technique.models import Technique
from forms import RequirementForm, PersonInfoForm, PracticeForm, ManagerForm, PracticeModelForm, LPracticeForm
from utils import update_player_active_qset, sliding_window, check_manager_status

from GChartWrapper import GChart

def club_list(request):

    info_dict = {
        'queryset':Club.objects.all(),
        'template_name':'Dojo/Club_object_list.html'
    }

    return list_detail.object_list(request, **info_dict)

def search(request):
    print request.DATA

def club_detail(request, club = None):

    club = get_object_or_404(Club, Slug = club)

    if request.method == 'POST':
        form = ManagerForm(request.POST)

        if form.is_valid() and check_manager_status(request, club):
            remove = form.cleaned_data['Remove']
            user = form.cleaned_data['User']
            if remove:
                club.Managers.remove(user)
                messages.success(request, '%s was removed as a manager for  %s.' % (user.username, club.Name))
            else:
                club.Managers.add(user)
                messages.success(request, '%s was added as a manager for  %s.' % (user.username, club.Name))
            return HttpResponseRedirect(club.get_absolute_url())


    else:
        form = ManagerForm()

    info_dict = {
        'club':club,
        'template_name':'Dojo/Club_object_detail.html',
        'manager_form':form

    }

    return render_to_response('Dojo/Club_object_detail.html', info_dict,
                              context_instance = RequestContext(request))

def check_club(request, club = None):
    club = get_object_or_404(Club, Slug = club)
    members = set(club.Members.all())
    
    for practice in club.practice_set.order_by('Date'):
        for pr in practice.practicerecord_set.all():
            if pr.Person not in members:
                mr = MemberRecord(Person = pr.Person, 
                                    DateOccured = practice.Date,
                                    Club = club)
                mr.save()
                messages.success(request, '%s was added succeessfuly to the club.' % pr.Person.Name)
    update_player_active_qset(club.Members.all(), club, request = request)
    
    return HttpResponseRedirect(club.get_absolute_url())
    

def practice_list(request, club = None):

    club = get_object_or_404(Club, Slug = club)
    practices = club.practice_set.all().annotate(NumPeople = Count('person')).order_by('-Date')
    if practices.count() > 10:
        chart = GChart(ctype = 'line')
        data = sliding_window(practices)
        chart.dataset(data[:500]).axes.type('xy')
    

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
        if form.is_valid() and check_manager_status(request, club):
            person = form.cleaned_data.get('Person', None)
            if person is None and len(form.cleaned_data['New_person']) > 0:
                person, isnew = Person.objects.get_or_create(Name = form.cleaned_data['New_person'])
                person.save()
                mr = MemberRecord(Person = person,
                                  Club = club,
                                  DateOccured = practice.Date)
                mr.save()
                rr = RankRecord(Rank = 'White', Person = person, DateOccured = practice.Date)
                rr.save()
                messages.success(request, '%s was added succeessfuly to %s as a White belt.' % (person.Name, club.Name))
            if person is not None:

                pr, new_r = PracticeRecord.objects.get_or_create(Practice = practice,
                                                            DateOccured = practice.Date,
                                                            Person = person)
                if new_r:
                    messages.success(request, '%s was added succeessfuly to this practice.' % person.Name)
                if not person.memberrecord_set.filter(Club = club).exists():
                    mr = MemberRecord(Person = person,
                                  Club = club,
                                  DateOccured = practice.Date)
                    mr.save()

                if not person.memberrecord_set.filter(Club = club).latest().is_active:
                    prevmr = person.memberrecord_set.filter(Club = club).latest()
                    days_gone =  (prevmr.DateOccured - practice.Date).days
                    mr = MemberRecord(Person = person,
                                  Club = club,
                                  DateOccured = practice.Date)
                    mr.save()
                    messages.success(request, '%s came back after %i days of inactivity!' % (person.Name, abs(days_gone)))
            
            tech = form.cleaned_data.get('Technique', None)
            if tech is None and len(form.cleaned_data['New_technique']) > 0:
                print 'form', form.cleaned_data['New_technique'] is None
                tech, isnew = Technique.objects.get_or_create(Name = form.cleaned_data['New_technique'])

            if tech:
                practice.technique_set.add(tech)
                messages.success(request, 'Sucessfully added the %s Technique' % tech.Name)
               
            

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
    else:
        club_obj = None

    request.session['last_page'] = request.path
    info_dict = {
        'club':club_obj
    }

    return render_to_response('Dojo/Person_object_list.html', info_dict,
                              context_instance = RequestContext(request))
@login_required
def person_detail(request, id = None):

    person = get_object_or_404(Person, id = int(id))
    clubs = person.club_set.all().distinct()
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
                make_messages(request, person, new_p, ('Name', 'Email', 'is_instructor'))
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

def club_landing(request):
    
    if request.method == 'POST':
        form = LPracticeForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
        
    messages.error(request, 'Could not create the practice')
    return HttpResponseRedirect(request.session.get('last_page', reverse('home_site')))


def make_messages(request, oitem, nitem, fields):
    func = attrgetter(*fields)
    for field, ores, nres in zip(fields, func(oitem), func(nitem)):
        if ores != nres:
            request.success('Changed %s to %s' % (field, nres))
