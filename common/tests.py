from datetime import datetime

import pytest
import pytz
from django.test import SimpleTestCase

from .utils import *


@pytest.mark.django_db
class TestQuarterWeekToMonthWeek(SimpleTestCase):
    def test_quarter_week_to_month_week(self):
        result1 = quarter_week_to_month_week(1, 1)
        result2 = quarter_week_to_month_week(4, 15)
        result3 = quarter_week_to_month_week(3, 5)

        assert (1, 1) == result1
        assert (12, 5) == result2
        assert (7, 5) == result3


@pytest.mark.django_db
class TestGetDeadlineGoal(SimpleTestCase):
    def test_year(self):
        year1 = 2022
        year2 = 2021

        result1 = get_deadline_goal(year1)
        result2 = get_deadline_goal(year2)

        assert result1 == datetime(2023, 1, 1)
        assert result2 == datetime(2022, 1, 2)

    def test_quarter(self):
        year = 2022
        quarter1 = 1
        quarter2 = 3

        result1 = get_deadline_goal(year, quarter1)
        result2 = get_deadline_goal(year, quarter2)

        assert result1 == datetime(2022, 4, 3)
        assert result2 == datetime(2022, 10, 2)

    def test_month(self):
        year = 2022
        month1 = 4
        month2 = 8

        result1 = get_deadline_goal(year, month=month1)
        result2 = get_deadline_goal(year, month=month2)

        assert result1 == datetime(2022, 5, 1)
        assert result2 == datetime(2022, 9, 4)

    def test_year_quarter_week(self):
        result1 = get_deadline_goal(2022, 1, week=8)
        result2 = get_deadline_goal(2022, 3, week=4)

        assert result1 == datetime(2022, 2, 27)
        assert result2 == datetime(2022, 7, 31)

    def test_year_month_week(self):
        result1 = get_deadline_goal(2022, month=5, week=2)
        result2 = get_deadline_goal(2022, month=9, week=4)

        assert result1 == datetime(2022, 5, 15)
        assert result2 == datetime(2022, 10, 2)
