from models import *
from django.db.models import Count
from datetime import timedelta, date
from django.contrib import messages



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





