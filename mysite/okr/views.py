
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .forms import KeyResultForm, ObjectiveForm, MonthResultForm, ActionForm
from .models import Objective, Action, MonthResult, KeyResultSuggestion
from .services import generate_month_results


def index(request):
    objectives = Objective.objects.all()
    goal = objectives.filter(year=timezone.now().year).first().goal if objectives.exists() else "Jūsų metai"
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

    if request.method == 'POST':
        month_result_id = request.POST.get('month_result_id')
        month_result = get_object_or_404(MonthResult, id=month_result_id)
        form = MonthResultForm(request.POST, instance=month_result)
        if form.is_valid():
            form.save()
        return redirect('dashboard', pk=pk)

    return render(request, 'dashboard.html', {
        'objective': objective,
        'current_month_num': current_month_num,
    })

def action_items(request, year, month, kr_id):
    month_result = get_object_or_404(
        MonthResult,
        id=kr_id,
        month=month,
        monthly_key_result__objective__year=year,
    )

    if request.method == 'POST':
        if request.POST.get('form_type') == 'month_result':
            form = MonthResultForm(request.POST, instance=month_result)
            if form.is_valid():
                form.save()
        elif request.POST.get('form_type') == 'action':
            action_form = ActionForm(request.POST)
            if action_form.is_valid():
                action = action_form.save(commit=False)
                action.month_result = month_result
                action.save()
        return redirect('dashboard', pk=month_result.monthly_key_result.objective.pk)
    else:
        form = MonthResultForm(instance=month_result)
        action_form = ActionForm()

    return render(request, 'actions.html', {
        'month_result': month_result,
        'actions': month_result.action_set.all(),
        'form': form,
        'action_form': action_form,
    })

def month_result_calc(request, objective_pk):
    if request.method == 'POST':
        form = KeyResultForm(request.POST)
        if form.is_valid():
            key_result = form.save(commit=False)
            key_result.objective = Objective.objects.get(pk=objective_pk)
            key_result.save()
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

def month_result_calc(request, objective_pk):
    suggestions = KeyResultSuggestion.objects.all()

    if request.method == 'POST':
        form = KeyResultForm(request.POST)
        if form.is_valid():
            key_result = form.save(commit=False)
            key_result.objective = Objective.objects.get(pk=objective_pk)
            key_result.save()
            generate_month_results(key_result)
            return redirect('dashboard', pk = key_result.objective.pk)
    else:
        form = KeyResultForm()

    return render(request, 'month_result_calc.html', {
        'form': form,
        'suggestions': suggestions
    })

def update_month_form(request):
    if request.method == 'POST':
        form = MonthResultForm(request.POST)
        if form.is_valid():
            actual_result = form.save()
            return redirect('dashboard', pk=month_resutl)
    else:
        form = MonthResultForm()

    return render(request, 'actions.html', {'form': form})