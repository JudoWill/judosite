from django.db import models

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

    def __unicode__(self):
        return self.Slug

class Person(models.Model):
    Name = models.CharField(max_length = 255)
    Email = models.EmailField(null = True, blank = True, default = None)
    is_instructor = models.BooleanField(default = False)
    Rank = models.ManyToManyField('RankRecord')
    Requirements = models.ManyToManyField('Requirement',
                                          through = 'RequirementRecord')
    PracticeAttended = models.ManyToManyField('Practice',
                                              through = 'PracticeRecord')
    Picture = models.ImageField(upload_to = 'pictures', null = True,
                                blank = True, default = None)

    def __unicode__(self):
        return self.Name

class Requirement(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField()
    URL = models.URLField(verify_exists = False)
    Valid_for = models.IntegerField()

    def __unicode__(self):
        return self.Slug

class Practice(models.Model):
    Club = models.ManyToManyField(Club)
    Date = models.DateField()

    def __unicode__(self):
        return '<%s:%s>' % (self.Club, self.Date)

#Record models
class RequirementRecord(PersonRecord):
    Requirement = models.ForeignKey(Requirement)


    def __unicode__(self):
        return self._base_unicode(self.Requirement)


class PracticeRecord(PersonRecord):
    Practice = models.ForeignKey(Practice)

    def __unicode__(self):
        return self._base_unicode(self.Practice)

    def _get_date(self):
        return self.Practice.Date

    DateOccured = property(_get_date)

class MemberRecord(PersonRecord):
    Club = models.ForeignKey(Club)
    is_active = models.BooleanField(default = True)

    def __unicode__(self):
        return self._base_unicode(self.Club)

class RankRecord(PersonRecord):
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

    def __unicode__(self):
        return self._base_unicode(self.Rank)