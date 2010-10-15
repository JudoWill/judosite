from models import *
from django.db import models
from django.db.models import Count, Max


class TechniqueManager(models.Manager):
    def club_qset(self, club):
        qset = super(TechniqueManager, self).get_query_set()
        if club is not None:
            qset = qset.filter(Practices__Club = club)
        qset = qset.annotate(num_practice = Count('Practices'))
        qset = qset.annotate(last_practice = Max('Practices__Date'))

        return qset
