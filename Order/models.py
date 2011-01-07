from django.db import models
from Dojo.models import Person
from django.core.urlresolvers import reverse

# Create your models here.

class GiOrder(models.Model):
    
    person = models.ForeignKey(Person)
    gitype = models.ForeignKey('GiType')
    closed = models.BooleanField(default = False)
    paid = models.BooleanField(default = False)
    date = models.DateField()

    class Meta:
        ordering = ['date', 'person']    

    def __unicode__(self):
        return ':'.join([str(self.person), str(self.gitype), str(self.date)])

    def get_absolute_url(self):
        return reverse('order_detail', kwargs = {'ID': self.pk})

class OrderStatus(models.Model):
    
    order = models.ForeignKey(GiOrder)    
    date = models.DateField()
    status = models.CharField(max_length = 20,
                            choices = (('Requested','Requested'),
                                        ('Placed','Placed'),
                                        ('Delivered','Delivered')))

    class Meta:
        ordering = ['-date']
        get_latest_by = 'date'
        

    def __unicode__(self):
        return ':'.join([str(self.order), self.status, str(self.date)])


class GiType(models.Model):
    
    description = models.CharField(max_length = 255)
    color = models.CharField(max_length = 10, choices = (('White', 'White'), 
                                                        ('Blue', 'Blue')))
    price = models.IntegerField()
    size = models.IntegerField()


    def __unicode__(self):
        return str(self.description) + ':' + str(self.size)+ ':' + str(self.color)
