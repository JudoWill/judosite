from django.db import models

# Create your models here.

class PersonRecord(models.Model):
    Person = models.ForeignKey('Person')
    DateOccured = models.DateField()

    class Meta:
        abstract = True


class Club(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField()
    Members = models.ManyToManyField('Person', through = 'MemberRecord')

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

class Requirement(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField()
    URL = models.URLField(verify_exists = False)
    Valid_for = models.IntegerField()

class Practice(models.Model):
    Club = models.ManyToManyField(Club)
    Date = models.DateField()

#Record models
class RequirementRecord(PersonRecord):
    Requirement = models.ForeignKey(Requirement)


class PracticeRecord(PersonRecord):
    Practice = models.ForeignKey(Practice)


    def _get_date(self):
        return self.Practice.Date

    DateOccured = property(_get_date)

class MemberRecord(PersonRecord):
    Club = models.ForeignKey(Club)
    is_active = models.BooleanField(default = True)

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
