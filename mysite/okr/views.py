
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Objective, Action, ActionComment

from .forms import KeyResultForm, ObjectiveForm, MonthResultForm, ActionForm, ActionUpdateForm
from .models import Objective, Action, MonthResult, KeyResultSuggestion
from .services import generate_month_results
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from datetime import datetime
import json
from django.core.serializers.json import DjangoJSONEncoder

@login_required
def index(request):
    objectives = Objective.objects.filter(user=request.user)
    current_year = datetime.now().year
    last_year = current_year - 1
    current_objective = objectives.filter(year=current_year).first()
    last_objective = objectives.filter(year=last_year).first()

    if not objectives.exists():
        return redirect('onboarding')

    goal = objectives.filter(year=timezone.now().year).first().goal if objectives.exists() else "Jūsų metai"
    brand = objectives.first().brand if objectives.exists() else "Jūsų Brand"
    # Grafiko duomenys
    charts_data = []
    if current_objective:
        for kr in current_objective.keyresult_set.all():
            months = kr.monthresult_set.order_by('month')
            charts_data.append({
                'name': kr.name,
                'planned': [float(m.planned_result) for m in months],
                'actual': [float(m.actual_result) if m.actual_result else None for m in months],
                'months': [m.get_month_display() for m in months],
            })

    return render(request, 'index.html',
                  {'objectives': objectives,
                   'current_year': current_year,
                   'last_year': last_year,
                   'goal': goal,
                   'current_objective': current_objective,
                   'last_objective': last_objective,
                   'brand': brand,
                   'charts_data': json.dumps(charts_data, cls=DjangoJSONEncoder),
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
        elif request.POST.get('form_type') == 'add_comment':
            action_id = request.POST.get('action_id')
            text = request.POST.get('comment_text')
            if action_id and text:
                action = get_object_or_404(Action, id=action_id)
                ActionComment.objects.create(
                    action=action,
                    user=request.user,
                    text=text
                )
        return redirect('action_items', year=year, month=month, kr_id=kr_id)
    else:
        form = MonthResultForm(instance=month_result)
        action_form = ActionForm()

    return render(request, 'actions.html', {
        'month_result': month_result,
        'actions': month_result.action_set.all(),
        'form': form,
        'action_form': action_form,
        'objective': month_result.monthly_key_result.objective,
        'kr': month_result.monthly_key_result,
    })

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
    objective = get_object_or_404(Objective, pk=objective_pk, user=request.user)

    if request.method == 'POST':
        form = KeyResultForm(request.POST)
        if form.is_valid():
            key_result = form.save(commit=False)
            key_result.objective = objective  # tiesiog naudoji jau turimą objektą
            key_result.save()
            generate_month_results(key_result)
            if 'save_and_add' in request.POST:
                return redirect('key_result_create', objective_pk=objective.pk)
            return redirect('dashboard', pk=objective.pk)

    else:
        form = KeyResultForm()

    return render(request, 'month_result_calc.html', {
        'form': form,
        'objective': objective,
        'suggestions': suggestions
    })

@login_required
def update_month_form(request):
    if request.method == 'POST':
        form = MonthResultForm(request.POST)
        if form.is_valid():
            actual_result = form.save()
            return redirect('dashboard', pk=month_result)
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


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(ActionComment, id=comment_id, user=request.user)

    # Išsaugome kur grįžti po trynimo
    action = comment.action
    month_result = action.month_result

    comment.delete()

    return redirect('action_items',
                    year=month_result.monthly_key_result.objective.year,
                    month=month_result.month,
                    kr_id=month_result.id)