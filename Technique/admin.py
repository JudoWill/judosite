from django.contrib import admin
from models import *

class TagAdmin(admin.ModelAdmin):
    actions = ['Join_Tag']
    def Join_Tag(self, request, queryset):
        keep_tag = queryset[0]
        techs = set(keep_tag.Technique.all())
        for tag in queryset[1:]:
            for tech in tag.Technique.all():
                if tech not in techs:
                    keep_tag.technique.add(tech)
                    techs.add(tech)
            tag.delete()


admin.site.register(TechniqueTag, TagAdmin)
admin.site.register(Technique)