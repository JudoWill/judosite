from django.contrib import admin
from models import *


class PersonAdmin(admin.ModelAdmin):
    actions = ['Join_People']
    def Join_People(self, request, queryset):
        keep_per = queryset[0]
        for per in queryset[1:]:
            for prac in per.practicerecord_set.all():
                prac.Person = keep_per
                prac.save()
            per.delete()

admin.site.register(Club)

# Debugging admin
admin.site.register(Person, PersonAdmin)
admin.site.register(Requirement)
admin.site.register(Practice)

class RequirementRecordAdmin(admin.ModelAdmin):
    list_display = ['Person', 'DateOccured', 'Requirement']

admin.site.register(RequirementRecord, RequirementRecordAdmin)
admin.site.register(PracticeRecord)
admin.site.register(MemberRecord)
admin.site.register(RankRecord)
