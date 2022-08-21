from datetime import datetime

import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from common.utils import get_current_quarter

from .models import (GoalModel, MonthEnum, QuarterEnum, StatusEnum, TimeModel,
                     TimeTypeEnum)


@pytest.mark.django_db
class GoalViewTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = get_user_model().objects.create_user(
            username="test user", email="user@example.com", password="testpass123"
        )

        self.other_user = get_user_model().objects.create_user(
            username="other test user",
            email="otheruser@example.com",
            password="testpass123",
        )

        backlog_time = TimeModel.objects.create(type=None)

        self.backlog_goal = GoalModel.objects.create(
            name="Backlog goal 1",
            due_time=backlog_time,
            status=StatusEnum.NONE,
            user=self.user,
        )

        planned_time = TimeModel.objects.create(type=TimeTypeEnum.YEAR, year=2022)

        self.planned_goal = GoalModel.objects.create(
            name="Planned goal 1",
            due_time=planned_time,
            status=StatusEnum.NONE,
            user=self.user,
        )

        current_time = TimeModel.objects.create(type=TimeTypeEnum.YEAR, year=2022)

        self.current_goal = GoalModel.objects.create(
            name="Current goal 1",
            due_time=current_time,
            status=StatusEnum.WIP,
            user=self.user,
        )

        archive_time = TimeModel.objects.create(type=TimeTypeEnum.YEAR, year=2022)

        self.archived_goal = GoalModel.objects.create(
            name="Archived goal 1",
            due_time=archive_time,
            status=StatusEnum.DONE,
            user=self.user,
        )

    def test_access_by_other_user(self):
        self.client.login(email=self.other_user.email, password="testpass123")
        response = self.client.get(reverse("backlog_goals"))

        assert response.status_code == 200
        assert not "Backlog goal 1" in response.rendered_content
        assert "goals/lists/backlog_goal_list.html" in [
            t.name for t in response.templates
        ]

    def test_backlog_goal_list(self):
        self.client.login(email=self.user.email, password="testpass123")
        response = self.client.get(reverse("backlog_goals"))

        assert response.status_code == 200
        assert "Backlog goal 1" in response.rendered_content
        assert "goals/lists/backlog_goal_list.html" in [
            t.name for t in response.templates
        ]

    def test_planned_goal_list(self):
        self.client.login(email=self.user.email, password="testpass123")
        response = self.client.get(reverse("planned_goals"))

        assert response.status_code == 200
        assert "Planned goal 1" in response.rendered_content
        assert "goals/lists/planned_goal_list.html" in [
            t.name for t in response.templates
        ]

    def test_current_goal_list(self):
        self.client.login(email=self.user.email, password="testpass123")
        response = self.client.get(reverse("current_goals"))

        assert response.status_code == 200
        assert "Current goal 1" in response.rendered_content
        assert "goals/lists/current_goal_list.html" in [
            t.name for t in response.templates
        ]

    def test_archive_goal_list(self):
        self.client.login(email=self.user.email, password="testpass123")
        response = self.client.get(reverse("archive_goals"))

        assert response.status_code == 200
        assert "Archived goal 1" in response.rendered_content
        assert "goals/lists/archive_goal_list.html" in [
            t.name for t in response.templates
        ]


@pytest.mark.django_db
class GoalTests(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = get_user_model().objects.create_user(
            username="test user", email="user@example.com", password="testpass123"
        )

    def test_backlog(self):
        time = TimeModel.objects.create(type=None)

        goal = GoalModel.objects.create(
            name="Test backlog", due_time=time, user=self.user
        )

        assert goal in GoalModel.objects.is_backlog()

    def test_planned_year(self):
        time = TimeModel.objects.create(
            type=TimeTypeEnum.YEAR.value, year=datetime.now().year
        )

        goal = GoalModel.objects.create(
            name="Test planned year", due_time=time, user=self.user
        )

        assert goal in GoalModel.objects.is_planned()

    def test_planned_quarter(self):
        time = TimeModel.objects.create(
            type=TimeTypeEnum.QUARTER.value,
            year=datetime.now().year,
            quarter=get_current_quarter() + 1,
        )

        goal = GoalModel.objects.create(
            name="Test planned quarter", due_time=time, user=self.user
        )

        assert goal in GoalModel.objects.is_planned()

    def test_planned_month(self):
        time = TimeModel.objects.create(
            type=TimeTypeEnum.MONTH.value,
            year=datetime.now().year,
            month=datetime.now().month,
        )

        goal = GoalModel.objects.create(
            name="Test planned month", due_time=time, user=self.user
        )

        assert goal in GoalModel.objects.is_planned()

    def test_planned_year_quarter(self):
        year_time = TimeModel.objects.create(
            type=TimeTypeEnum.YEAR.value, year=datetime.now().year
        )

        year_goal = GoalModel.objects.create(
            name="Test planned year", due_time=year_time, user=self.user
        )

        quarter_time = TimeModel.objects.create(
            type=TimeTypeEnum.QUARTER.value, quarter=get_current_quarter() + 1
        )

        quarter_goal = GoalModel.objects.create(
            name="Test planned year quarter",
            parent_goal=year_goal,
            due_time=quarter_time,
            user=self.user,
        )

        assert (
            quarter_goal
            in GoalModel.objects.is_planned().get(id=year_goal.id).goals.all()
        )

    def test_planned_year_month(self):
        year_time = TimeModel.objects.create(
            type=TimeTypeEnum.YEAR.value, year=datetime.now().year
        )

        year_goal = GoalModel.objects.create(
            name="Test planned year", due_time=year_time, user=self.user
        )

        month_time = TimeModel.objects.create(
            type=TimeTypeEnum.MONTH.value, month=datetime.now().month
        )

        month_goal = GoalModel.objects.create(
            name="Test planned year month",
            parent_goal=year_goal,
            due_time=month_time,
            user=self.user,
        )

        assert (
            month_goal
            in GoalModel.objects.is_planned().get(id=year_goal.id).goals.all()
        )

    def test_planned_year_quarter_week(self):
        year_time = TimeModel.objects.create(
            type=TimeTypeEnum.YEAR.value, year=datetime.now().year
        )

        year_goal = GoalModel.objects.create(
            name="Test planned year", due_time=year_time, user=self.user
        )

        quarter_time = TimeModel.objects.create(
            type=TimeTypeEnum.QUARTER.value, quarter=get_current_quarter() + 1
        )

        quarter_goal = GoalModel.objects.create(
            name="Test planned year quarter",
            parent_goal=year_goal,
            due_time=quarter_time,
            user=self.user,
        )

        week_time = TimeModel.objects.create(type=TimeTypeEnum.WEEK.value, week=14)

        week_goal = GoalModel.objects.create(
            name="Test planned year quarter week",
            parent_goal=quarter_goal,
            due_time=week_time,
            user=self.user,
        )

        assert (
            week_goal
            in GoalModel.objects.is_planned()
            .get(id=year_goal.id)
            .goals.get(id=quarter_goal.id)
            .goals.all()
        )

    def test_planned_year_month_week(self):
        year_time = TimeModel.objects.create(
            type=TimeTypeEnum.YEAR.value, year=datetime.now().year
        )

        year_goal = GoalModel.objects.create(
            name="Test planned year", due_time=year_time, user=self.user
        )

        month_time = TimeModel.objects.create(
            type=TimeTypeEnum.MONTH.value, month=datetime.now().month
        )

        month_goal = GoalModel.objects.create(
            name="Test planned year month",
            parent_goal=year_goal,
            due_time=month_time,
            user=self.user,
        )

        week_time = TimeModel.objects.create(type=TimeTypeEnum.WEEK.value, week=4)

        week_goal = GoalModel.objects.create(
            name="Test planned year month week",
            parent_goal=month_goal,
            due_time=week_time,
            user=self.user,
        )

        assert (
            week_goal
            in GoalModel.objects.is_planned()
            .get(id=year_goal.id)
            .goals.get(id=month_goal.id)
            .goals.all()
        )
