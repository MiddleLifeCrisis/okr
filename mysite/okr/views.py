from django.shortcuts import render, get_object_or_404
from .models import YearObjective

def index(request):
    objectives = YearObjective.objects.all()
    return render(request, 'index.html', {'objectives': objectives})

def dashboard(request, pk):
    objective = get_object_or_404(YearObjective, pk=pk)
    return render(request, 'dashboard.html', {'objective': objective})