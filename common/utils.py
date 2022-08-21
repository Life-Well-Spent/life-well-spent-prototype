from datetime import datetime, timedelta

import pytz
from django.utils import timezone

EVEN_MONTHS = [4, 6, 9, 11]
ODD_MONTHS = [1, 3, 5, 7, 8, 10, 12]


def quarter_week_to_month_week(quarter, week):
    month_number = (week - 1) // 5
    month = ((quarter - 1) * 3) + (month_number + 1)
    week = week - month_number * 5

    return (month, week)


def get_current_quarter():
    today = timezone.now()

    if today.month < 3:
        return 1

    if today.month < 6:
        return 2

    if today.month < 9:
        return 3

    if today.month < 12:
        return 4


def get_deadline_goal(year, quarter=None, month=None, week=None):
    initial_month = month
    initial_week = week

    if month is None:
        month = 12

    if week is None and not quarter is None:
        week = 14
    elif week is None and quarter is None:
        week = 4

    result = datetime.min
    result.replace(tzinfo=pytz.UTC)

    if not quarter is None:
        month, week = quarter_week_to_month_week(quarter, week)

    # Get first day of month
    first_day = datetime(year=year, month=month, day=1, tzinfo=pytz.UTC)
    if first_day.weekday() != 0:
        week = week + 1

    days = week * 7 - first_day.weekday() - 1
    if initial_month == month and initial_week is None:
        if month in EVEN_MONTHS and days < 30:
            days = days + 7
        elif month in ODD_MONTHS and days < 31:
            days = days + 7
        elif month == 2 and days < 28:
            days = days + 7

    result = result.replace(year=year, month=month)
    result = result + timedelta(days=days)

    return result
