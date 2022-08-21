from django.db import models
from django.db.models import Q
from django.utils import timezone

from .models.enums.status import StatusEnum


class GoalManager(models.Manager):
    def base(self):
        return self.filter(parent_goal=None)

    def is_backlog(self):
        return self.filter(due_time__type=None)

    def is_planned(self):
        today = timezone.now()
        today_weekday = today.weekday()
        first_weekday = today.replace(day=today.day - today_weekday)
        last_weekday = first_weekday.replace(day=first_weekday.day + 7)

        return self.base().filter(
            ~Q(due_time__type=None)
            & Q(due_time__calculated__gt=last_weekday)
            & Q(status=None)
        )

    def is_current(self):
        today = timezone.now()
        today_weekday = today.weekday()
        first_weekday = today.replace(day=today.day - today_weekday)
        last_weekday = first_weekday.replace(day=first_weekday.day + 7)

        return self.base().filter(
            ~Q(due_time__type=None)
            & (
                Q(due_time__calculated__range=(first_weekday, last_weekday))
                | Q(due_time__calculated__lt=today)
                | Q(status=StatusEnum.WIP)
            )
        )

    def is_archive(self):
        return self.base().filter(
            ~Q(due_time__type=None)
            & (Q(status=StatusEnum.DONE) | Q(status=StatusEnum.CANCELLED))
        )
