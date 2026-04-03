from django.contrib import admin
from .models import Unit, YearObjective, YearKeyResult, MonthResult, Action

class ActionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'month_result')

class MonthResultAdmin(admin.ModelAdmin):
    list_display = ('monthly_key_result', 'month')



admin.site.register(Unit)
admin.site.register(Action, ActionsAdmin)
admin.site.register(YearObjective)
admin.site.register(YearKeyResult)
admin.site.register(MonthResult,MonthResultAdmin)