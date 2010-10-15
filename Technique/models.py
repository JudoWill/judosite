from django.db import models
from Dojo.models import Practice
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

# Create your models here.
class Technique(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField(editable = False)

    Practices = models.ManyToManyField(Practice)

    def save(self, *args, **kwargs):
        self.Slug = slugify(self.Name)
        super(Technique, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.Name

    def get_absolute_url(self):
        return reverse('technique_detail', kwargs = {'technique':self.Slug})

class TechniqueTag(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField(editable = False)
    Technique = models.ManyToManyField(Technique)

    def save(self, *args, **kwargs):
        self.Slug = slugify(self.Name)
        super(TechniqueTag, self).save(*args, **kwargs)


    def __unicode__(self):
        return self.Slug

    def get_absolute_url(self):
        return reverse('tag_detail', kwargs = {'tag':self.Slug})