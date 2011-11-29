from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from Dojo.models import Person
from Technique.models import Technique, TechniqueTag
from autocomplete.views import autocomplete
from django.contrib.auth.models import User

autocomplete.register(
        id = 'student',
        queryset = Person.objects.all(),
        fields = ('Name', ),
        limit = 5,
    )
autocomplete.register(
    id = 'technique',
    queryset = Technique.objects.all(),
    fields = ('Name', ),
    limit = 5
)
autocomplete.register(
    id = 'techniquetag',
    queryset = TechniqueTag.objects.all(),
    fields = ('Slug', ),
    limit = 5
)
autocomplete.register(
    id = 'users',
    queryset = User.objects.all(),
    fields = ('username', ),
    limit = 5
)


urlpatterns = patterns('django.views.generic.simple',
                       (r'^judosite/home.html', 'direct_to_template', {'template': 'index.html'}, 'home_site'),
                       )


urlpatterns += patterns('',
    # Example:
    # (r'^judosite/', include('judosite.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^judosite/admin/', include(admin.site.urls)),
    url(r'judosite/login.html', 'django.contrib.auth.views.login', name = 'login'),
	url(r'judosite/logout.html', 'django.contrib.auth.views.logout', name = 'logout'),
    (r'^judosite/Dojo/', include('Dojo.urls')),
    (r'^judosite/Technique/', include('Technique.urls')),
    (r'^judosite/GiOrder/', include('Order.urls')),
    url('^judosite/autocomplete/(\w+)/$', autocomplete, name='autocomplete'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^judosite/site_media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_FILE_ROOT}),
        (r'^judosite/js/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.STATIC_FILE_ROOT+'/js/'})
    )
