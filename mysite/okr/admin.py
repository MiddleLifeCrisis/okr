from django.contrib import admin
from .models import Objective, KeyResult, Initiative, KPI

admin.site.register(KPI)
admin.site.register(Objective)
admin.site.register(KeyResult)
admin.site.register(Initiative)