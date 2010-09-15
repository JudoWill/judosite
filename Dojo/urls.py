from django.conf.urls.defaults import *
from django.conf import settings
from views import *


urlpatterns = patterns('django.views.generic.simple',
                       (r'^home.html', 'direct_to_template', {'template': 'index.html'}),
                       )

urlpatterns += patterns('',
                       url(r'^club_list.html', club_list, name = 'club_list'),
                       url(r'^(P<club>[\w-]+)/club_detail.html', club_detail, name = 'club_detail'),
                       url(r'^(P<club>[\w-]+)/practice_list.html', practice_list, name = 'practice_list'),
                       url(r'^(P<club>[\w-]+)/(P<id>\d+)/practice_detail.html', practice_detail, name = 'practice_detail'),
                       url(r'^(P<club>[\w-]+)/person_list.html', person_list, name = 'person_list'),
                       url(r'^(P<club>[\w-]+)/(P<id>\d+)/person_detail.html', person_detail, name = 'person_list'),
                       )

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_FILE_ROOT}),
    )