from django import forms
from django.conf import settings
from django.db.models.query_utils import Q
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from models import *
from autocomplete.fields import ModelChoiceField

class LocalModelChoiceField(ModelChoiceField):

    class Media:
        extend = False
        css = {'all':
            (' ',)#"autocomplete.css"
        }
        #js = ('http://yui.yahooapis.com/combo'
        #      '?2.6.0/build/yahoo-dom-event/yahoo-dom-event.js'
        #      # decomment to enable animation.
        #      #'&2.6.0/build/animation/animation-min.js'
        #      '&2.6.0/build/connection/connection-min.js'
        #      '&2.6.0/build/datasource/datasource-min.js'
        #      '&2.6.0/build/autocomplete/autocomplete-min.js',
        #      'js/yui_autocomplete.js')
        

