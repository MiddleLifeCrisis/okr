from django.db import models


class Objective(models.Model):
    """
    Strateginis lygmuo: 26 metų tikslas (kokybinis)
    Pvz.: 'Tapti regiono rinkos lyderiais'
    """
    title = models.CharField(max_length=255)
    year = models.IntegerField(default=2026)
    mission_vision = models.TextField(default="Profit is not a strategy, it's a result of good strategy.")

    def __str__(self):
        return f"{self.year} Tikslas: {self.title}"


class KeyResult(models.Model):
    """
    Taktinis lygmuo: Pamatuojami rezultatai
    Pvz.: '1.2 M metinė apyvarta' arba 'Įsidiegti CRM'
    """
    KR_TYPE_CHOICES = [
        ('QUANTITATIVE', 'Kiekybinis (Outcome-based)'),
        ('PROJECT', 'Project-based (Pabaigta/Nepabaigta)'),
    ]

    objective = models.ForeignKey(Objective, on_delete=models.CASCADE, related_name='key_results')
    title = models.CharField(max_length=255)
    kr_type = models.CharField(max_length=20, choices=KR_TYPE_CHOICES, default='QUANTITATIVE')

    # Rezultato matavimas (skaičiams)
    target_value = models.FloatField(null=True, blank=True, help_text="Tikslas (pvz. 1.2)")
    current_value = models.FloatField(default=0, help_text="Dabartinė reikšmė (pvz. 0.4)")
    unit = models.CharField(max_length=50, blank=True, help_text="Vienetas: mln EUR, ROI, d.d.")

    # Rezultato matavimas (projektams)
    is_completed = models.BooleanField(default=False)

    def progress_percentage(self):
        """Suskaičiuoja progresą procentais"""
        if self.kr_type == 'PROJECT':
            return 100 if self.is_completed else 0
        if self.target_value and self.target_value > 0:
            return min(round((self.current_value / self.target_value) * 100, 2), 100)
        return 0

    def __str__(self):
        return f"KR: {self.title}"


class Initiative(models.Model):
    """
    Operacinis lygmuo: Iniciatyvos ir veiksmai
    Pvz.: '100 cold calls', 'Rasti 3 bandymui'
    """
    key_result = models.ForeignKey(KeyResult, on_delete=models.CASCADE, related_name='initiatives')
    title = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)

    # Galime pridėti pastabų lauką specifiniams KPI (kaip CTR tavo schemoje)
    notes = models.TextField(blank=True, help_text="Papildomi KPI, pvz. CTR - 20%")

    def __str__(self):
        return f"Iniciatyva: {self.title}"

class KPI(models.Model):
    name = models.CharField(max_length=100)
    current_value = models.FloatField()
    target_value = models.FloatField()
    unit = models.CharField(max_length=20, default='€') # Pvz. %, €, vnt.

    @property
    def status_color(self):
        # Paprasta logika: jei pasiekta 90% - žalia, jei 50% - geltona, mažiau - raudona
        ratio = self.current_value / self.target_value
        if ratio >= 0.9: return "text-green-500"
        if ratio >= 0.5: return "text-yellow-500"
        return "text-red-500"