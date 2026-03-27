from django.shortcuts import render
from .models import Objective, KPI  # Importuojame abu modelius


def dashboard(request):
    objectives = Objective.objects.prefetch_related('key_results').all()
    kpis = KPI.objects.all()  # Paimame visus KPI

    context = {
        'objectives': objectives,
        'kpis': kpis,  # Perduodame į šabloną
    }
    return render(request, 'okr/dashboard.html', context)