from django.conf.urls.defaults import *
from django.conf import settings
from views import *


urlpatterns = patterns('',
                        url(r'order_list.html', order_list, name = 'order_list'),
                        url(r'(?P<ID>\d+)/order_detail.html', order_detail, name = 'order_detail'))
