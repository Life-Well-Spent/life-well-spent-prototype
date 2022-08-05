from django.urls import path

from .views import HelloWorldView

urlpatterns = [
    path('', HelloWorldView.as_view(), name="hello_world")
]