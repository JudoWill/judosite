# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.forms.models import inlineformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext

from models import *
from forms import *


def order_list(request):
    
    if request.method == 'POST':
        form = NewOrder(request.POST)
        if form.is_valid():
            order = form.save(commit = False)
            order.save()
            
            return HttpResponseRedirect(order.get_absolute_url())
    else:
        form = NewOrder()


    info_dict = {
        'queryset':GiOrder.objects.filter(closed = False),
        'template_name':'Order/GiOrder_object_list.html',
        'extra_context':{'form':form}
    }

    return list_detail.object_list(request, **info_dict)

def order_detail(request, ID = None):
    
    order = get_object_or_404(GiOrder, pk = ID)
    OrderStatusFormset = inlineformset_factory(GiOrder, OrderStatus)    
    if request.method == 'POST':
        formset = OrderStatusFormset(request.POST, instance = order)
        if formset.is_valid():
            formset.save()
    else:
        formset = OrderStatusFormset(instance = order)

    info_dict = {
            'order':order,
            'formset':formset
            }

    return render_to_response('Order/GiOrder_object_detail.html', info_dict, 
                                context_instance = RequestContext(request))
