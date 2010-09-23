from django.db import models
from django.core.urlresolvers import reverse

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
    Slug = models.SlugField()
    Members = models.ManyToManyField('Person', through = 'MemberRecord')

    class Meta:
        get_latest_by = 'Name'
        ordering = ['Name']

    def __unicode__(self):
        return self.Slug

    def get_absolute_url(self):
        return reverse('club_detail', kwargs = {'club': self.Slug})

    def get_instructors(self):
        return self.Members.filter(is_instructor = True)

    def get_students(self):
        return self.Members.filter(is_instructor = False)

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

    class Meta:
        ordering = ['Name']

    def __unicode__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('person_detail', kwargs = {'id':self.id})

class Requirement(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField()
    URL = models.URLField(default = None, blank = True, null = True,
                          verify_exists = False)
    Valid_for = models.IntegerField()
    Club = models.ForeignKey(Club, default = None, null = True)

    class Meta:
        get_latest_by = 'Name'
        ordering = ['Name']

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