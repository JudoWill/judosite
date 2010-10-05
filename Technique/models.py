from django.db import models
from Dojo.models import Practice

# Create your models here.
class Technique(models.Model):
    Name = models.CharField(max_length = 255)
    Slug = models.SlugField()

    Practices = models.ManyToManyField(Practice)

class TechniqueTag(models.Model):
    Slug = models.SlugField()
    Technique = models.ManyToManyField(Technique)