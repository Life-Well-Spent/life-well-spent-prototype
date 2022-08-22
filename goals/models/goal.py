import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from common.models import TimeStampedModel
from goals.managers import GoalManager

from .enums.status import StatusEnum
from .time import TimeModel


class GoalModel(TimeStampedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=1, choices=StatusEnum.choices, null=True, default=None
    )
    parent_goal = models.ForeignKey(
        "self", null=True, on_delete=models.SET_NULL, related_name="goals"
    )
    due_time = models.ForeignKey(TimeModel, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    started = models.DateTimeField(null=True)
    finished = models.DateTimeField(null=True)

    objects = GoalManager()

    def is_overdue(self):
        today = timezone.now().date()
        return (
            not self.due_time.type is None
            and not self.due_time.is_same_week(today)
            and self.due_time.calculated < today
        )

    def __str__(self):
        return f"{self.name} (Due: {self.due_time})"

    def save(self, *args, **kwargs):
        if self.parent_goal:
            self.due_time.year = self.parent_goal.due_time.year

            if self.parent_goal.due_time.quarter:
                self.due_time.quarter = self.parent_goal.due_time.quarter

            if self.parent_goal.due_time.month:
                self.due_time.month = self.parent_goal.due_time.month

            self.due_time.save()

        if self.status == StatusEnum.WIP:
            self.started = timezone.now()

        if self.status == StatusEnum.DONE or self.status == StatusEnum.CANCELLED:
            self.finished = timezone.now()

        return super(GoalModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.due_time.delete()
        return super(GoalModel, self).delete(*args, **kwargs)
