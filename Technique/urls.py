from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
                       url(r'list.html', technique_list, name = 'technique_list'),
                       url(r'(?P<technique>[\w-]*)/detail.html', technique_detail, name = 'technique_detail'))