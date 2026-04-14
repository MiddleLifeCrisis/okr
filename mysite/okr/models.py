from django.db import models
from django.contrib.auth.models import User

class Unit(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name


class Objective(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brand = models.CharField(max_length=100, default='Your Brand', verbose_name="Prekinis ženklas",)
    team = models.CharField(max_length=200, default='Your Department', verbose_name="Atsakingas asmuo arba komanda",)
    year = models.IntegerField(default='2026', verbose_name="Metai",)
    goal = models.CharField(max_length=200, verbose_name="Tikslas",)
    def __str__(self):
        return f"{self.year} - {self.goal} "


class KeyResult(models.Model):
    DISTRIBUTION_CHOICES = [
        ('cumulative', 'Išdaliniamas per mėnesius (÷ 12)'),
        ('fixed', 'Vienodas procentas viesiems mėn'),
        ('binary', 'Įvykdyta / Neįvykdyta')
    ]

    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    annual_goal = models.DecimalField(max_digits=12, decimal_places=2)
    icon_class = models.CharField(max_length=50, default="fa-rocket")

    distribution_type = models.CharField(
        max_length=20,
        choices=DISTRIBUTION_CHOICES,
        default='cumulative',
    )

    def __str__(self):
        return f"{self.name} ({self.objective.year})"

class KeyResultSuggestion(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class MonthResult(models.Model):
# 1. Pirmiausia aprašom pasirinkimus
    MONTH_CHOICES = [
        (1, 'Sausis'), (2, 'Vasaris'), (3, 'Kovas'), (4, 'Balandis'),
        (5, 'Gegužė'), (6, 'Birželis'), (7, 'Liepa'), (8, 'Rugpjūtis'),
        (9, 'Rugsėjis'), (10, 'Spalis'), (11, 'Lapkritis'), (12, 'Gruodis'),
    ]

    QUARTER_CHOICES = [(1, 'Q1'), (2, 'Q2'), (3, 'Q3'), (4, 'Q4')]

    monthly_key_result = models.ForeignKey(KeyResult, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MONTH_CHOICES, default=1)
    quarter = models.IntegerField(choices=QUARTER_CHOICES, default=1)
    planned_result = models.DecimalField(max_digits=12, decimal_places=1)
    actual_result = models.DecimalField(max_digits=12, decimal_places=1, null=True, blank=True)

    @property
    def achievement_percentage(self):
        if self.planned_result and self.actual_result:
            return (self.actual_result / self.planned_result) * 100
        return 0

    def __str__(self):
        # Naudojam get_month_display(), kad matytume tekstą, o ne skaičių
        return f"{self.monthly_key_result} | {self.month} | "

class Action(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    month_result = models.ForeignKey(MonthResult, on_delete=models.CASCADE)
    action_item = models.CharField(max_length=200)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True)
    planned_result = models.DecimalField(max_digits=12, decimal_places=1)
    actual_result = models.DecimalField(max_digits=12, decimal_places=1, null=True, blank=True)
    is_done= models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True, verbose_name="Komentarai / Problemos sprendimas")

    @property
    def action_achievement_percentage(self):
        if self.planned_result and self.actual_result:
            return (self.actual_result / self.planned_result) * 100
        return 0

    def __str__(self):
        status = "✅" if self.is_done else "❌"
        return f"{status} {self.action_item} | {self.month_result}"


