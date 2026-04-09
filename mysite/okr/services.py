from decimal import Decimal

from .models import MonthResult


def generate_month_results(key_result):
    QUARTER_MAP = {1:1, 2:1, 3:1, 4:2, 5:2, 6:2, 7:3, 8:3, 9:3, 10:4, 11:4, 12:4}

    for month_num in range(1,13):
        if key_result.distribution_type == 'cumulative':
            planned_result = (key_result.annual_goal / Decimal('12')).quantize(Decimal('0.1'))
        elif key_result.distribution_type == 'fixed':
            planned_result = key_result.annual_goal
        elif key_result.distribution_type == 'binary':
            planned_result = Decimal('1')

        MonthResult.objects.get_or_create(
            monthly_key_result=key_result,
            month=month_num,
            defaults={
                'quarter': QUARTER_MAP[month_num],
                'planned_result': planned_result,
            }
        )