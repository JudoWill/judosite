from django.conf.urls.defaults import *
from django.views.generic import list_detail
from models import *
from views import *




urlpatterns = patterns('',
                       url(r'^dojo_list.html', dojo_list, name = 'dojo_list'),
                       url(r'^(P<dojo>[\w-]+)/dojo_detail.html', dojo_detail, name = 'dojo_detail'),
                       url(r'^(P<dojo>[\w-]+)/practice_list.html', practice_list, name = 'practice_list'),
                       url(r'^(P<dojo>[\w-]+)/(P<id>\d+)/practice_detail.html', practice_detail, name = 'practice_detail'),
                       url(r'^(P<dojo>[\w-]+)/person_list.html', person_list, name = 'person_list'),
                       url(r'^(P<dojo>[\w-]+)/(P<id>\d+)/person_detail.html', person_detail, name = 'person_list'),
                       )