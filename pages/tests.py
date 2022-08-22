import pytest
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


@pytest.mark.django_db
class HomeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test user", email="user@example.com", password="testpass123"
        )

        self.super_user = get_user_model().objects.create_user(
            username="test superuser",
            email="superuser@example.com",
            password="testpass123",
            is_superuser=True,
        )

        self.url = reverse("home")
        self.response = self.client.get(self.url)

    def test_status_code(self):
        assert self.response.status_code == 200

    def test_template(self):
        assert "pages/home.html" in (t.name for t in self.response.templates)

        assert "Log in" in self.response.rendered_content

        assert "Log in" in self.response.rendered_content
        self.client.login(email=self.super_user.email, password="testpass123")
        response = self.client.get(self.url)
        assert "Log out" in response.rendered_content

    def test_superuser(self):
        self.client.login(email=self.super_user.email, password="testpass123")
        response = self.client.get(self.url)

        assert "Admin" in response.rendered_content
