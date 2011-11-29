from models import *
from django.db import models
from django.db.models import Count, Max


class PersonManager(models.Manager):
    def club_qset(self, club):
        qset = super(PersonManager, self).get_query_set()
        if club is not None:
            qset = qset.filter(practicerecord__Practice__Club = club)
        qset = qset.annotate(num_practice = Count('practicerecord'))
        qset = qset.annotate(last_practice = Max('practicerecord__DateOccured'))

        return qset

    def time_window_qset(self, start_date, end_date, club):

        qset = super(PersonManager, self).get_query_set()
        qset = qset.filter(practicerecord__Practice__Club = club,
                           practicerecord__Practice__Date__gte = start_date,
                           practicerecord__Practice__Date__lte = end_date)
        qset = qset.distinct()
        qset = qset.annotate(num_practice=Count('practicerecord'))

        return qset

        