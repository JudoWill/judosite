from django.contrib import admin
from models import *
from django.contrib import messages

class GiOrderAdmin(admin.ModelAdmin):
    actions = ['Close_Orders']
    list_display = ['person', 'gitype', 'closed', 'paid', 'date']

    def Close_Orders(self, request, queryset):
        num = queryset.update(closed = True)
        messages.success(request, 'Closed %i orders' % num)

class GiTypeAdmin(admin.ModelAdmin):
    list_display = ['description', 'color', 'weave', 'size', 'price']


admin.site.register(GiOrder, GiOrderAdmin)
admin.site.register(GiType, GiTypeAdmin)

