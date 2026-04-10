from django.contrib import admin
from .models import Unit, Objective, KeyResult, MonthResult, Action, KeyResultSuggestion


class ActionsAdmin(admin.ModelAdmin):
    list_display = ('action_item', 'month_result')

class MonthResultAdmin(admin.ModelAdmin):
    list_display = ('monthly_key_result', 'month')



admin.site.register(Unit)
admin.site.register(Action, ActionsAdmin)
admin.site.register(Objective)
admin.site.register(KeyResult)
admin.site.register(MonthResult,MonthResultAdmin)
admin.site.register(KeyResultSuggestion)