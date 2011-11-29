from django.conf.urls.defaults import *
from django.conf import settings
from views import *


urlpatterns = patterns('',
                       url(r'club_list.html', club_list, name = 'club_list'),
                       url(r'(?P<club>[\w-]*)/club_detail.html', club_detail, name = 'club_detail'),
                       url(r'(?P<club>[\w-]*)/check_club.html', check_club, name = 'club_check'),
                       url(r'(?P<club>[\w-]+)/practice_list.html', practice_list, name = 'practice_list'),
                       url(r'(?P<club>[\w-]+)/(?P<id>\d+)/practice_detail.html', practice_detail, name = 'practice_detail'),
                       url(r'(?P<club>[\w-]+)/person_list.html', person_list, name = 'person_list_by_club'),
                       url(r'person_list.html', person_list, name = 'person_list'),
                       url(r'(?P<id>\d+)/person_detail.html', person_detail, name = 'person_detail'),
                       url(r'(?P<slug>[\w-]+)/requirement_detail.html', requirement_detail, name = 'requirement_detail'),
                       url(r'requirements.html', requirement_list, name = 'requirement_list'),
                       url(r'search.html', search, name = 'person_search'),
                       url(r'practice_landing.html', club_landing, name = 'practice_form_landing'),
                       )
