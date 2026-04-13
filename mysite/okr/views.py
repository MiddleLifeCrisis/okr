
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic

from .forms import KeyResultForm, ObjectiveForm, MonthResultForm, ActionForm, ActionUpdateForm
from .models import Objective, Action, MonthResult, KeyResultSuggestion
from .services import generate_month_results
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm


@login_required
def index(request):
    objectives = Objective.objects.filter(user=request.user)

    if not objectives.exists():
        return redirect('onboarding')

    goal = objectives.filter(year=timezone.now().year).first().goal if objectives.exists() else "Jūsų metai"
    brand = objectives.first().brand if objectives.exists() else "Jūsų Brand"
    return render(request, 'index.html',
                  {'objectives': objectives,
                   'goal': goal,
                   'brand': brand
                   })

@login_required
def dashboard(request, pk):
    objective = get_object_or_404(Objective, pk=pk, user=request.user)
    current_month_num = int(request.GET.get('month', timezone.now().month))
    current_month_num = max(1, min(12, current_month_num))

    if request.method == 'POST':
        month_result_id = request.POST.get('month_result_id')
        month_result = get_object_or_404(MonthResult, id=month_result_id)
        form = MonthResultForm(request.POST, instance=month_result)
        if form.is_valid():
            form.save()
        return redirect(f'/dashboard/{pk}/?month={current_month_num}')

    return render(request, 'dashboard.html', {
        'objective': objective,
        'current_month_num': current_month_num,
    })

@login_required
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
        elif request.POST.get('form_type') == 'action_update':
            action_id = request.POST.get('action_id')
            action = get_object_or_404(Action, id=action_id)
            action_update_form = ActionUpdateForm(request.POST, instance=action)
            if action_update_form.is_valid():
                action_update_form.save()
        return redirect('action_items', year=year, month=month, kr_id=kr_id)
    else:
        form = MonthResultForm(instance=month_result)
        action_form = ActionForm()

    return render(request, 'actions.html', {
        'month_result': month_result,
        'actions': month_result.action_set.all(),
        'form': form,
        'action_form': action_form,
    })

@login_required
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

@login_required
def onboarding (request):
    if request.method == 'POST':
        form = ObjectiveForm(request.POST)
        if form.is_valid():
            objective = form.save(commit=False)
            objective.user = request.user
            objective.save()
            return redirect('key_result_create', objective_pk=objective.pk)
    else:
        form = ObjectiveForm()

    return render(request, 'onboarding.html', {'form': form})

@login_required
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

@login_required
def update_month_form(request):
    if request.method == 'POST':
        form = MonthResultForm(request.POST)
        if form.is_valid():
            actual_result = form.save()
            return redirect('dashboard', pk=month_resutl)
    else:
        form = MonthResultForm()

    return render(request, 'actions.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})

@login_required
def action_delete(request, pk):
    action = get_object_or_404(Action, pk=pk)
    if request.method == 'POST':
        month_result = action.month_result
        action.delete()
        return redirect('action_items',
                       year=month_result.monthly_key_result.objective.year,
                       month=month_result.month,
                       kr_id=month_result.id)
    return redirect('action_items',
                   year=action.month_result.monthly_key_result.objective.year,
                   month=action.month_result.month,
                   kr_id=action.month_result.id)