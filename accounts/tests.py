import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from goals.models import GoalModel, StatusEnum, TimeModel, TimeTypeEnum

from .views import DeleteAccountView


@pytest.mark.django_db
class SettingsViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user", email="user@example.com", password="testpass123"
        )

        self.url = reverse("settings")

        self.client.login(email=self.user.email, password="testpass123")
        self.response = self.client.get(self.url)

    def test_status_code(self):
        assert self.response.status_code == 200

    def test_template(self):
        assert "accounts/settings.html" in (t.name for t in self.response.templates)


@pytest.mark.django_db
class DeleteAccountViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user", email="user@example.com", password="testpass123"
        )

        time = TimeModel.objects.create(type=TimeTypeEnum.YEAR, year=2022)

        self.goal = GoalModel.objects.create(
            name="Backlog goal 1",
            due_time=time,
            status=StatusEnum.NONE,
            user=self.user,
        )

    def test_delete_account_view(self):
        self.client.login(email=self.user.email, password="testpass123")
        self.client.post(reverse("delete_account"))

        assert not self.goal in GoalModel.objects.all()
