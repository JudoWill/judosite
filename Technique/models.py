from django.db import models
from Dojo.models import Practice
from django.core.urlresolvers import reverse

# Create your models here.
class Technique(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField()

    Practices = models.ManyToManyField(Practice)

    def __unicode__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('technique_detail', kwargs = {'technique':self.Slug})

class TechniqueTag(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField()
    Technique = models.ManyToManyField(Technique)

    def __unicode__(self):
        return self.Slug

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs = {'tag':self.Slug})