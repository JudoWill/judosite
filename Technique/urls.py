from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
                       url(r'list.html', technique_list, name = 'technique_list'))