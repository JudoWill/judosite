from django.db import models
from django.db.models import Count, Max
from django.core.urlresolvers import reverse
from datetime import date
from utils import get_missing_reqs
from managers import *
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class PersonRecord(models.Model):
    Person = models.ForeignKey('Person')
    DateOccured = models.DateField()

    class Meta:
        abstract = True

    def _base_unicode(self, arg):
        return '<%s:%s:%s>' % (arg, self.Person, self.DateOccured)


class Club(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField(editable = False)
    Members = models.ManyToManyField('Person', through = 'MemberRecord')
    Managers = models.ManyToManyField(User)

    class Meta:
        get_latest_by = 'Name'
        ordering = ['Name']
    
    def save(self, *args, **kwargs):
        self.Slug = slugify(self.Name)
        super(Club, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.Slug

    def get_absolute_url(self):
        return reverse('club_detail', kwargs = {'club': self.Slug})

    def get_instructors(self):
        qset = self.Members.filter(is_instructor = True)
        qset = qset.annotate(last_practice = Max('practicerecord__DateOccured'),
                                PracticeNum = Count('practicerecord'))

        return qset

    def get_students(self):
        qset = self.Members.filter(is_instructor = False)
        qset = qset.annotate(last_practice = Max('practicerecord__DateOccured'),
                                PracticeNum = Count('practicerecord'))

        return qset

    def get_active_members(self):
        aqset =  self.Members.annotate(na = Count('practicerecord'))
        return aqset.filter(memberrecord__is_active = True).filter(na__gte = 3)

class Person(models.Model):
    Name = models.CharField(max_length = 255)
    Email = models.EmailField(null = True, blank = True, default = None)
    is_instructor = models.BooleanField(default = False)
    Requirements = models.ManyToManyField('Requirement',
                                          through = 'RequirementRecord')
    PracticeAttended = models.ManyToManyField('Practice',
                                              through = 'PracticeRecord')
    Picture = models.ImageField(upload_to = 'pictures', null = True,
                                blank = True, default = None)
    Gender = models.CharField(max_length = 10, default = 'Male',
                              choices = (('Male', 'Male'),
                                         ('Female', 'Female')))
    objects = PersonManager()
    class Meta:
        ordering = ['Name']

    def __unicode__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('person_detail', kwargs = {'id':self.id})

    def is_active(self, club = None):
        if club:
            return self.memberrecord_set.filter(Club = club).latest().is_active
        else:
            return self.memberrecord_set.latest().is_active

    def check_missing_reqs(self, clubs = None, date_check = date.today()):
        return get_missing_reqs(self, clubs = clubs, date_check = date_check)


class Requirement(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField(editable = False)
    URL = models.URLField(default = None, blank = True, null = True,
                          verify_exists = False)
    Valid_for = models.IntegerField()
    Club = models.ForeignKey(Club, default = None, null = True)

    class Meta:
        get_latest_by = 'Name'
        ordering = ['Name']

    def save(self, *args, **kwargs):
        self.Slug = slugify(self.Name)
        super(Requirement, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.Slug

    def get_absolute_url(self):
        return reverse('requirement_detail', kwargs = {'slug':self.Slug})

class Practice(models.Model):
    Club = models.ForeignKey(Club, default = None, null = True)
    Date = models.DateField()

    class Meta:
        get_latest_by = 'Date'
        ordering = ['Club', 'Date']

    def __unicode__(self):
        return '<%s:%s>' % (self.Club, self.Date)

    def get_absolute_url(self):
        print {'club':self.Club.Slug, 'id':self.id}
        return reverse('practice_detail', args = (), kwargs = {'club':self.Club.Slug,
                                                    'id':self.id})

#Record models
class RequirementRecord(PersonRecord):
    Requirement = models.ForeignKey(Requirement)

    class Meta:
        get_latest_by = 'DateOccured'
        ordering = ['Requirement', 'DateOccured']

    def __unicode__(self):
        return self._base_unicode(self.Requirement)


class PracticeRecord(PersonRecord):
    Practice = models.ForeignKey(Practice)

    class Meta:
        get_latest_by = 'DateOccured'
        ordering = ['Practice', 'DateOccured']

    def __unicode__(self):
        return self._base_unicode(self.Practice)

    

class MemberRecord(PersonRecord):
    Club = models.ForeignKey(Club)
    is_active = models.BooleanField(default = True)

    class Meta:
        get_latest_by = 'DateOccured'
        ordering = ['Club', 'DateOccured']

    def __unicode__(self):
        return self._base_unicode(self.Club)

class RankRecord(models.Model):
    Person = models.ForeignKey(Person, default = None, null = True)
    DateOccured = models.DateField()
    rank_choices = [('White', 'White'),
                    ('Yellow', 'Yellow'),
                    ('Orange', 'Orange'),
                    ('Green', 'Green'),
                    ('Sankyu', 'Sankyu'),
                    ('Nikyu', 'Nikyu'),
                    ('Ikyu', 'Ikyu'),
                    ('Shodan', 'Shodan'),
                    ('Nidan', 'Nidan'),
                    ('Sandan', 'Sandan')]

    Rank = models.CharField(max_length = 255,
                            choices = rank_choices)

    class Meta:
        get_latest_by = 'DateOccured'
        ordering = ['DateOccured', 'Rank']

    def __unicode__(self):
        return '<%s:%s>' % (self.Rank, self.DateOccured)