from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
                       url(r'technique_list.html', technique_list, name = 'technique_list'),
                       url(r'(?P<technique>[\w-]*)/detail.html', technique_detail, name = 'technique_detail'),
                       url(r'tag_list.html', tag_list, name = 'tag_list'),
                       url(r'(?P<tag>[\w-]*)/detail.html', tag_detail, name = 'tag_detail'),)