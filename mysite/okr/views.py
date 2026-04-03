from datetime import timezone
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from .models import YearObjective

def index(request):
    objectives = YearObjective.objects.all()
    return render(request, 'index.html', {'objectives': objectives})

def dashboard(request, pk):
    objective = get_object_or_404(YearObjective, pk=pk)
    current_month_num = timezone.now().month
    return render(request, 'dashboard.html', {'objective': objective,
                                              'current_month_num': current_month_num
                                              })