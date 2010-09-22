from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from Dojo.models import Person
from autocomplete.views import autocomplete

autocomplete.register(
        id = 'student',
        queryset = Person.objects.all(),
        fields = ('Name', ),
        limit = 5,
    )


urlpatterns = patterns('django.views.generic.simple',
                       (r'^home.html', 'direct_to_template', {'template': 'index.html'}),
                       )


urlpatterns += patterns('',
    # Example:
    # (r'^judosite/', include('judosite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    url(r'login.html', 'django.contrib.auth.views.login', name = 'login'),
	url(r'logout.html', 'django.contrib.auth.views.logout', name = 'logout'),
    (r'^Dojo/', include('Dojo.urls')),
    url('^autocomplete/(\w+)/$', autocomplete, name='autocomplete'),    

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_FILE_ROOT}),
        (r'^js/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_FILE_ROOT+'/js/'})
    )