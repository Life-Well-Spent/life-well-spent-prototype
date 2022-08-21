from django.template.defaulttags import register
from django.utils import timezone


@register.filter
def overdue(goal_list):
    result = []

    for goal in goal_list:
        if goal.is_overdue():
            result.append(goal)

    return result


@register.filter
def not_overdue(goal_list):
    result = []

    for goal in goal_list:
        if not goal.is_overdue():
            result.append(goal)

    return result
