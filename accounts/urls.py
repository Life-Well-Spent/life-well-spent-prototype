from django.urls import path

from .views import DeleteAccountView, SettingsView

urlpatterns = [
    path("settings", SettingsView.as_view(), name="settings"),
    path("delete", DeleteAccountView.as_view(), name="delete_account"),
]
