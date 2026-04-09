
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import KeyResultForm, ObjectiveForm
from .models import Objective, Action, MonthResult
from .services import generate_month_results


def index(request):
    objectives = Objective.objects.all()
    goal = objectives.get(year=timezone.now().year).goal if objectives.exists() else "Jūsų metai"
    # goal = Objective.objects.first().goal - tas pats tik trumpiau
    brand = objectives.first().brand if objectives.exists() else "Jūsų Brand"
    return render(request, 'index.html',
                  {'objectives': objectives,
                   'goal': goal,
                   'brand': brand
                   })

def dashboard(request, pk):
    objective = get_object_or_404(Objective, pk=pk)
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

    return render(request, 'actions.html', {
        'month_result': month_result,
        'actions': month_result.action_set.all()
    })

def month_result_calc(request):
    if request.method == 'POST':
        form = KeyResultForm(request.POST)
        if form.is_valid():
            key_result = form.save()
            generate_month_results(key_result)
            return redirect('dashboard', pk = key_result.objective.pk)
    else:
        form = KeyResultForm()

    return render(request, 'month_result_calc.html', {'form': form})

def onboarding (request):
    if request.method == 'POST':
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            objective = form.save()
            return redirect('dashboard', pk = objective.pk)
    else:
        form = ObjectiveForm()

    return render(request, 'onboarding.html', {'form': form})