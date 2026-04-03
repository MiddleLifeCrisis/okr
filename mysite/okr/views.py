from datetime import timezone
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import YearObjective, Action, MonthResult


def index(request):
    objectives = YearObjective.objects.all()
    return render(request, 'index.html', {'objectives': objectives})

def dashboard(request, pk):
    objective = get_object_or_404(YearObjective, pk=pk)
    current_month_num = timezone.now().month
    return render(request, 'dashboard.html', {'objective': objective,
                                              'current_month_num': current_month_num
                                              })

def action_items(request, year, month, kr_id):
    month_result = get_object_or_404(
        MonthResult,
        id=kr_id,
        month=month,
        monthly_key_result__objective__year=year,
    )

    action_items = month_result.action_set.all()

    return render(request, 'actions.html', {
        'month_result': month_result,
        'action_items': action_items,
    })