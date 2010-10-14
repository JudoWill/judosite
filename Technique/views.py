# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.db.models import Count, Max
from django.views.generic import list_detail
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from Dojo.models import *
from Technique.models import *
from forms import *


def technique_list(request):
    
    if request.method == 'POST':
        form = TechniqueForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
    else:
        form = TechniqueForm()
    
    info_dict = {
        'queryset':Technique.objects.all(),
        'form':form
    }

    return render_to_response('Technique/Technique_object_list.html', info_dict,
                                context_instance = RequestContext(request))
    
    
    
def technique_detail(request, technique = None):
    tech_obj = get_object_or_404(Technique, Slug = technique)
    
    info_dict = {
        'technique':tech_obj
    }
    
    return render_to_response('Technique/Technique_object_detail.html', info_dict,
                                context_instance = RequestContext(request))
                                
def tag_list(request):
    
    if request.method == 'POST':
        form = TechniqueTagForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.save()
            return HttpResponseRedirect(obj.get_absolute_url())
    else:
        form = TechniqueTagForm()
        
    
    info_dict = {
        'queryset':TechniqueTag.objects.all(),
        'form':form
    }
    
    return render_to_response('Technique/Tag_object_list.html', info_dict,
                                context_instance = RequestContext(request))
    
def tag_detail(request, tag = None):
    pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    