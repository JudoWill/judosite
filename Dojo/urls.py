from django.conf.urls.defaults import *
from django.views.generic import list_detail
from models import *
from views import *




urlpatterns = patterns('',
                       url(r'^club_list.html', club_list, name = 'club_list'),
                       url(r'^(P<club>[\w-]+)/club_detail.html', club_detail, name = 'club_detail'),
                       url(r'^(P<club>[\w-]+)/practice_list.html', practice_list, name = 'practice_list'),
                       url(r'^(P<club>[\w-]+)/(P<id>\d+)/practice_detail.html', practice_detail, name = 'practice_detail'),
                       url(r'^(P<club>[\w-]+)/person_list.html', person_list, name = 'person_list'),
                       url(r'^(P<club>[\w-]+)/(P<id>\d+)/person_detail.html', person_detail, name = 'person_list'),
                       )