import pytest
from django.test import SimpleTestCase
from django.urls import reverse


@pytest.mark.django_db
class HelloWorldTests(SimpleTestCase):
    def setUp(self):
        url = reverse("hello_world")
        self.response = self.client.get(url)
    def test_status_code(self):
        assert self.response.status_code == 200
    
    def test_template(self):
        assert "pages/hello_world.html" in (t.name for t in self.response.templates )