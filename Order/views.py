# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse

from models import *
from forms import *


def order_list(request):
    
    if request.method == 'POST':
        form = NOrder(request.POST)
        if form.is_valid():
            gi = form.cleaned_data['gi']
            order = GiOrder(person = form.cleaned_data['person'],
                            gitype = gi, date = form.cleaned_data['date'])
            order.save()
            OrderStatus(order = order, date = order.date, status = 'Requested').save()
            messages.success(request, 'Order was created for %s.' % order.person.Name)
            return HttpResponseRedirect(order.get_absolute_url())
    else:
        form = NOrder()


    info_dict = {
        'queryset':GiOrder.objects.filter(closed = False),
        'template_name':'Order/GiOrder_object_list.html',
        'extra_context':{'form':form}
    }

    return list_detail.object_list(request, **info_dict)

def order_detail(request, ID = None):
    
    order = get_object_or_404(GiOrder, pk = ID)
    OrderStatusFormset = inlineformset_factory(GiOrder, OrderStatus, max_num = 3)    
    if request.method == 'POST':
        formset = OrderStatusFormset(request.POST, instance = order)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'Order was updated for %s.' % order.person.Name)
            return HttpResponseRedirect(reverse('order_list'))
    else:
        formset = OrderStatusFormset(instance = order)

    info_dict = {
            'order':order,
            'formset':formset
            }

    return render_to_response('Order/GiOrder_object_detail.html', info_dict, 
                                context_instance = RequestContext(request))
