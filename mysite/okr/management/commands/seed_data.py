from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from okr.models import Unit, Objective, KeyResult, MonthResult, Action
from decimal import Decimal


class Command(BaseCommand):
    help = 'Sukuria demo duomenis prezentacijai'

    def handle(self, *args, **kwargs):
        self.stdout.write('🌱 Pradedame seed...')

        # ── 1. UNITS ──────────────────────────────────────────
        eur, _ = Unit.objects.get_or_create(name='EUR')
        vnt, _ = Unit.objects.get_or_create(name='Vnt.')
        pct, _ = Unit.objects.get_or_create(name='%')
        calls, _ = Unit.objects.get_or_create(name='Skambučiai')
        leads, _ = Unit.objects.get_or_create(name='Leads')
        demo_u, _ = Unit.objects.get_or_create(name='Demo')
        tasks, _ = Unit.objects.get_or_create(name='Užduotys')

        # ── 2. USER ───────────────────────────────────────────
        user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@techflow.lt',
                'first_name': 'Demo',
                'last_name': 'Vartotojas',
            }
        )
        if created:
            user.set_password('demo1234')
            user.save()
            self.stdout.write('  ✅ User sukurtas: demo / demo1234')
        else:
            self.stdout.write('  ℹ️  User jau egzistuoja: demo')

        # ── 3. METAI ──────────────────────────────────────────
        self._create_2025(user, eur, vnt, pct)
        self._create_2026(user, eur, vnt, pct, calls, leads, demo_u, tasks)

        self.stdout.write(self.style.SUCCESS('✅ Seed baigtas!'))

    # ─────────────────────────────────────────────────────────
    # HELPER: quarter pagal mėnesį
    # ─────────────────────────────────────────────────────────
    def _q(self, month):
        return (month - 1) // 3 + 1

    # ─────────────────────────────────────────────────────────
    # HELPER: sukuria MonthResult įrašus
    # Grąžina sąrašą – vėliau naudosim Action'oms pridėti
    # ─────────────────────────────────────────────────────────
    def _months(self, kr, plan, actuals):
        results = []
        for i, actual in enumerate(actuals):
            month_num = i + 1
            mr = MonthResult.objects.create(
                monthly_key_result=kr,
                month=month_num,
                quarter=self._q(month_num),
                planned_result=Decimal(str(plan)),
                actual_result=Decimal(str(actual)) if actual is not None else None,
            )
            results.append(mr)
        return results

    # ─────────────────────────────────────────────────────────
    # HELPER: sukuria vieną Action įrašą
    # ─────────────────────────────────────────────────────────
    def _action(self, month_result, item, unit, planned, actual, is_done, notes=None):
        Action.objects.create(
            month_result=month_result,
            action_item=item,
            unit=unit,
            planned_result=Decimal(str(planned)),
            actual_result=Decimal(str(actual)) if actual is not None else None,
            is_done=is_done,
            notes=notes,
        )

    # ─────────────────────────────────────────────────────────
    # 2025 – tik rezultatai, be Action'ų
    # ─────────────────────────────────────────────────────────
    def _create_2025(self, user, eur, vnt, pct):
        obj = Objective.objects.create(
            user=user,
            brand='TechFlow UAB',
            team='Visa komanda',
            year=2025,
            goal='Tapti pirmuoju rinktinu SaaS sprendimu Baltijos rinkoje',
        )

        kr1 = KeyResult.objects.create(
            objective=obj, name='Metinės pajamos', unit=eur,
            annual_goal=Decimal('240000'), distribution_type='cumulative',
            icon_class='fa-euro-sign',
        )
        self._months(kr1, plan=20000, actuals=[
            15000, 16500, 18000, 19000, 20000, 21000,
            22000, 21500, 23000, 24000, 25000, 26000
        ])

        kr2 = KeyResult.objects.create(
            objective=obj, name='Aktyvūs mokantys klientai', unit=vnt,
            annual_goal=Decimal('48'), distribution_type='cumulative',
            icon_class='fa-users',
        )
        self._months(kr2, plan=4, actuals=[
            3, 4, 4, 5, 4, 4,
            5, 3, 4, 5, 4, 5
        ])

        kr3 = KeyResult.objects.create(
            objective=obj, name='NPS klientų pasitenkinimo balas', unit=pct,
            annual_goal=Decimal('75'), distribution_type='fixed',
            icon_class='fa-star',
        )
        self._months(kr3, plan=75, actuals=[
            60, 62, 63, 65, 66, 68,
            69, 70, 71, 73, 74, 75
        ])

        kr4 = KeyResult.objects.create(
            objective=obj, name='Kritinių bugų uždarymas per 24h', unit=pct,
            annual_goal=Decimal('90'), distribution_type='fixed',
            icon_class='fa-bug',
        )
        self._months(kr4, plan=90, actuals=[
            70, 75, 78, 80, 82, 85,
            87, 88, 89, 90, 91, 92
        ])

        kr5 = KeyResult.objects.create(
            objective=obj, name='Darbuotojų įsitraukimo indeksas', unit=pct,
            annual_goal=Decimal('80'), distribution_type='fixed',
            icon_class='fa-heart',
        )
        self._months(kr5, plan=80, actuals=[
            65, 66, 68, 69, 70, 72,
            73, 74, 75, 77, 78, 80
        ])

        self.stdout.write('  ✅ 2025 sukurta (12/12 mėn., be Action)')

    # ─────────────────────────────────────────────────────────
    # 2026 – 4 mėnesiai su Action'omis
    # Sausis–kovas: užbaigti. Balandis: tarpinis (~50%)
    # ─────────────────────────────────────────────────────────
    def _create_2026(self, user, eur, vnt, pct, calls, leads, demo_u, tasks):
        N = None  # mėnuo dar neįvyko

        obj = Objective.objects.create(
            user=user,
            brand='TechFlow UAB',
            team='Visa komanda',
            year=2026,
            goal='Iš augančios įmonės tapti lyderiu, kuris formuoja rinkos standartus',
        )

        # ── KR1: Metinės pajamos ──────────────────────────────
        kr1 = KeyResult.objects.create(
            objective=obj, name='Metinės pajamos', unit=eur,
            annual_goal=Decimal('300000'), distribution_type='cumulative',
            icon_class='fa-euro-sign',
        )
        mr1 = self._months(kr1, plan=25000, actuals=[
            24000, 26500, 28000,
            13500,  # balandis: ~50% tarpinis
            N, N, N, N, N, N, N, N
        ])

        # Sausis
        self._action(mr1[0], 'Šalti skambučiai potencialiems klientams', calls, 80, 72, True,
                     'Sunkiai sekėsi pasiekti sprendimų priėmėjus')
        self._action(mr1[0], 'Siųsti komercinius pasiūlymus', vnt, 20, 18, True)
        self._action(mr1[0], 'Upsell esamiems klientams', vnt, 5, 3, False,
                     'Du klientai atidėjo sprendimą iki vasario')

        # Vasaris
        self._action(mr1[1], 'Šalti skambučiai potencialiems klientams', calls, 80, 85, True,
                     'Peršokome planą – komanda motyvuota po sausio rezultatų')
        self._action(mr1[1], 'Siųsti komercinius pasiūlymus', vnt, 20, 22, True)
        self._action(mr1[1], 'Upsell esamiems klientams', vnt, 5, 5, True)

        # Kovas
        self._action(mr1[2], 'Šalti skambučiai potencialiems klientams', calls, 80, 78, True)
        self._action(mr1[2], 'Siųsti komercinius pasiūlymus', vnt, 20, 21, True)
        self._action(mr1[2], 'Pasiruošimas „Baltic Tech Expo" parodai', tasks, 10, 10, True,
                     'Paroda balandžio 18d. – visi materialai paruošti')

        # Balandis (tarpinis)
        self._action(mr1[3], 'Šalti skambučiai potencialiems klientams', calls, 80, 38, False,
                     'Mėnuo dar vyksta')
        self._action(mr1[3], 'Dalyvavimas „Baltic Tech Expo" parodoje', tasks, 1, 1, True,
                     'Surinkta 23 nauji kontaktai, 5 demo susitikimai suplanuoti')
        self._action(mr1[3], 'Siųsti komercinius pasiūlymus', vnt, 20, 9, False)

        # ── KR2: Aktyvūs mokantys klientai ───────────────────
        kr2 = KeyResult.objects.create(
            objective=obj, name='Aktyvūs mokantys klientai', unit=vnt,
            annual_goal=Decimal('60'), distribution_type='cumulative',
            icon_class='fa-users',
        )
        mr2 = self._months(kr2, plan=5, actuals=[
            5, 6, 7,
            3,  # balandis: tarpinis
            N, N, N, N, N, N, N, N
        ])

        # Sausis
        self._action(mr2[0], 'Demo prezentacijos potencialiems klientams', demo_u, 10, 8, True)
        self._action(mr2[0], 'Onboarding naujų klientų', vnt, 5, 5, True)

        # Vasaris
        self._action(mr2[1], 'Demo prezentacijos potencialiems klientams', demo_u, 10, 12, True,
                     'Papildomas demo ciklas po sausio rekomendacijų')
        self._action(mr2[1], 'Onboarding naujų klientų', vnt, 6, 6, True)

        # Kovas
        self._action(mr2[2], 'Demo prezentacijos potencialiems klientams', demo_u, 12, 14, True)
        self._action(mr2[2], 'Onboarding naujų klientų', vnt, 7, 7, True)

        # Balandis (tarpinis)
        self._action(mr2[3], 'Demo prezentacijos potencialiems klientams', demo_u, 12, 5, False,
                     'Mėnuo dar vyksta, 5 demo po parodos suplanuoti')
        self._action(mr2[3], 'Onboarding naujų klientų', vnt, 5, 3, False)

        # ── KR3: NPS balas ────────────────────────────────────
        kr3 = KeyResult.objects.create(
            objective=obj, name='NPS klientų pasitenkinimo balas', unit=pct,
            annual_goal=Decimal('85'), distribution_type='fixed',
            icon_class='fa-star',
        )
        mr3 = self._months(kr3, plan=85, actuals=[
            76, 78, 80,
            41,  # balandis: tarpinis (apklausa dar vyksta)
            N, N, N, N, N, N, N, N
        ])

        # Sausis
        self._action(mr3[0], 'Išsiųsti NPS apklausą klientams', vnt, 50, 47, True)
        self._action(mr3[0], 'Susisiekti su žemai įvertinusiais klientais', calls, 10, 8, True,
                     '2 klientai turėjo problemų su integracija – išspręsta')

        # Vasaris
        self._action(mr3[1], 'Išsiųsti NPS apklausą klientams', vnt, 50, 51, True)
        self._action(mr3[1], 'Susisiekti su žemai įvertinusiais klientais', calls, 8, 7, True)

        # Kovas
        self._action(mr3[2], 'Išsiųsti NPS apklausą klientams', vnt, 50, 50, True)
        self._action(mr3[2], 'Susisiekti su žemai įvertinusiais klientais', calls, 8, 8, True)
        self._action(mr3[2], 'Implementuoti top 3 klientų pasiūlymus', tasks, 3, 3, True,
                     'Pridėta bulk export funkcija ir pagerintas mobilusis view')

        # Balandis (tarpinis)
        self._action(mr3[3], 'Išsiųsti NPS apklausą klientams', vnt, 50, 24, False,
                     'Apklausa dar vyksta iki mėn. pabaigos')

        # ── KR4: Bugų uždarymas per 24h ───────────────────────
        kr4 = KeyResult.objects.create(
            objective=obj, name='Kritinių bugų uždarymas per 24h', unit=pct,
            annual_goal=Decimal('95'), distribution_type='fixed',
            icon_class='fa-bug',
        )
        mr4 = self._months(kr4, plan=95, actuals=[
            93, 95, 96,
            48,  # balandis: tarpinis
            N, N, N, N, N, N, N, N
        ])

        # Sausis
        self._action(mr4[0], 'Kritinių bugų peržiūra (daily standup)', tasks, 20, 19, True)
        self._action(mr4[0], 'On-call inžinieriaus budėjimas', tasks, 4, 4, True)

        # Vasaris
        self._action(mr4[1], 'Kritinių bugų peržiūra (daily standup)', tasks, 20, 20, True)
        self._action(mr4[1], 'On-call inžinieriaus budėjimas', tasks, 4, 4, True)
        self._action(mr4[1], 'Automatinių alertų konfigūracija', tasks, 5, 5, True,
                     'Sentry + Slack integracija – dabar reaguojame per <15min')

        # Kovas
        self._action(mr4[2], 'Kritinių bugų peržiūra (daily standup)', tasks, 20, 20, True)
        self._action(mr4[2], 'On-call inžinieriaus budėjimas', tasks, 4, 4, True)

        # Balandis (tarpinis)
        self._action(mr4[3], 'Kritinių bugų peržiūra (daily standup)', tasks, 20, 10, False,
                     'Mėnuo dar vyksta')
        self._action(mr4[3], 'On-call inžinieriaus budėjimas', tasks, 4, 2, False)

        # ── KR5: Darbuotojų įsitraukimas ──────────────────────
        kr5 = KeyResult.objects.create(
            objective=obj, name='Darbuotojų įsitraukimo indeksas', unit=pct,
            annual_goal=Decimal('88'), distribution_type='fixed',
            icon_class='fa-heart',
        )
        mr5 = self._months(kr5, plan=88, actuals=[
            81, 83, 85,
            43,  # balandis: tarpinis (apklausa dar vyksta)
            N, N, N, N, N, N, N, N
        ])

        # Sausis
        self._action(mr5[0], 'Mėnesinė komandos apklausa (pulse check)', vnt, 1, 1, True)
        self._action(mr5[0], '1:1 susitikimai su komandos nariais', vnt, 8, 7, True,
                     'Vienas narys atostogavo')

        # Vasaris
        self._action(mr5[1], 'Mėnesinė komandos apklausa (pulse check)', vnt, 1, 1, True)
        self._action(mr5[1], '1:1 susitikimai su komandos nariais', vnt, 8, 8, True)
        self._action(mr5[1], 'Komandos team building renginys', vnt, 1, 1, True,
                     'Escape room – puikios atsiliepimai, komanda labai patenkinta')

        # Kovas
        self._action(mr5[2], 'Mėnesinė komandos apklausa (pulse check)', vnt, 1, 1, True)
        self._action(mr5[2], '1:1 susitikimai su komandos nariais', vnt, 8, 8, True)
        self._action(mr5[2], 'Mokymai ir profesinio tobulėjimo sesija', vnt, 2, 2, True)

        # Balandis (tarpinis)
        self._action(mr5[3], 'Mėnesinė komandos apklausa (pulse check)', vnt, 1, 0, False,
                     'Apklausa išsiųsta, rezultatai renkami iki 30d.')
        self._action(mr5[3], '1:1 susitikimai su komandos nariais', vnt, 8, 4, False,
                     'Mėnuo dar vyksta')

        self.stdout.write('  ✅ 2026 sukurta (4/12 mėn. – balandis tarpinis)')