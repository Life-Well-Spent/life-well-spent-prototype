from datetime import datetime, timedelta

import pytz
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from common.utils import get_deadline_goal

from .enums.month import MonthEnum
from .enums.quarter import QuarterEnum
from .enums.timetype import TimeTypeEnum


class TimeModel(models.Model):
    type = month = models.CharField(
        max_length=1, choices=TimeTypeEnum.choices, null=True, default=TimeTypeEnum.NONE
    )
    year = models.PositiveSmallIntegerField(null=True)
    month = models.IntegerField(choices=MonthEnum.choices, null=True, default=None)
    quarter = models.IntegerField(choices=QuarterEnum.choices, null=True, default=None)
    week = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(52)], null=True
    )
    calculated = models.DateField(null=True)

    def save(self, *args, **kwargs):
        if self.type is None or (self.year is 0 or self.year is None):
            return super(TimeModel, self).save(*args, **kwargs)

        if self.type is TimeTypeEnum.YEAR.value:
            self.month = MonthEnum.NONE.value
            self.quarter = QuarterEnum.NONE.value
            self.week = None

        if self.type is TimeTypeEnum.QUARTER.value:
            self.month = MonthEnum.NONE.value
            self.week = None

        if self.type is TimeTypeEnum.MONTH.value:
            self.quarter = QuarterEnum.NONE.value
            self.week = None

        self.calculated = self.get_absolute_datetime()
        return super(TimeModel, self).save(*args, **kwargs)

    def get_absolute_datetime(self):
        year = int(self.year)
        quarter = (
            None if self.quarter is 0 or self.quarter is None else int(self.quarter)
        )
        month = None if self.month is 0 or self.month is None else int(self.month)
        week = None if self.week is None else int(self.week)

        return get_deadline_goal(year, quarter, month, week)

    def is_same_week(self, target):
        end_week = self.calculated
        start_week = end_week - timedelta(days=7)

        return target >= start_week and target <= end_week

    def __str__(self):
        if self.type == TimeTypeEnum.YEAR:
            return str(self.year)

        if self.type == TimeTypeEnum.QUARTER:
            return str(self.get_quarter_display())

        if self.type == TimeTypeEnum.MONTH:
            return str(self.get_month_display())

        if self.type == TimeTypeEnum.WEEK:
            return self.calculated.strftime("%Y-%m-%d")

        return ""
