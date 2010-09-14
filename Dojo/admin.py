from django.contrib import admin
from models import *

admin.site.register(Club)

# Debugging admin
admin.site.register(Person)
admin.site.register(Requirement)
admin.site.register(Practice)
admin.site.register(RequirementRecord)
admin.site.register(PracticeRecord)
admin.site.register(MemberRecord)
admin.site.register(RankRecord)
