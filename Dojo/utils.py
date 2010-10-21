from Dojo.models import *
from django.db.models import Count
from datetime import timedelta, date
from django.contrib import messages
from collections import deque
from itertools import islice
from operator import attrgetter



def check_player_active(person, club, days = 90, date_check = date.today()):
    """returns True for active players and False otherwise"""

    last_date = date_check-timedelta(days)
    qset = person.practicerecord_set.filter(DateOccured__gte = last_date)
    qset.exclude(DateOccured__gt = date_check) #deals with when I'm back-checking
    if club:
        qset.filter(Practice__Club = club)
    return qset.exists()


def update_player_active_qset(qset, club, days = 90, date_check = date.today(), request = None):

    for player in qset:
        cur_active = check_player_active(player, club, days = days,
                                         date_check = date_check)
        database_rec = player.memberrecord_set.filter(Club = club,
                                                      DateOccured__lte = date_check).latest()
        if cur_active != database_rec.is_active:
            mr = MemberRecord(Person = player, DateOccured = date_check,
                              Club = club, is_active = cur_active)
            mr.save()
            if request:
                if cur_active:
                    messages.success(request, '%s is now active!' % player.Name)
                else:
                    messages.success(request, '%s is now INACTIVE' % player.Name)


def sliding_window(qset, numfield = 'NumPeople', datefield = 'Date', winsize = 10):
    
    vgetter = attrgetter(numfield)
    qiter = qset.order_by('Date').iterator()
    win = deque([],winsize)
    
    vals = []
    for prac in qiter:
        win.append(vgetter(prac))
        vals.append(sum(win)/winsize)
        
    return vals
    


def get_missing_reqs(person, clubs = None, date_check = date.today()):

    missing = []
    if clubs is None:
        clubs = person.club_set.all()
    elif type(clubs) != type(Club.objects.all()): #only passed a single club
        clubs = Club.objects.filter(id = clubs.id)

    for club in clubs:
        for req in club.requirement_set.all():
            last_date = date_check - timedelta(req.Valid_for)
            qset = person.requirementrecord_set.filter(DateOccured__gte = last_date,
                                                       Requirement = req)
            if not qset.exists():
                missing.append(req)
    return missing
