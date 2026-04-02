from django.contrib import admin
from .models import Unit, YearObjective, YearKeyResult, MonthResult, Action



admin.site.register(Unit)
admin.site.register(Action)
admin.site.register(YearObjective)
admin.site.register(YearKeyResult)
admin.site.register(MonthResult)