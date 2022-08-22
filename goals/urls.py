from django.urls import path

from .views import (
    ArchiveView,
    BackLogView,
    CreateView,
    CurrentView,
    DeleteView,
    PlannedView,
    UpdateView,
)

urlpatterns = [
    path("backlog", BackLogView.as_view(), name="backlog_goals"),
    path("planned", PlannedView.as_view(), name="planned_goals"),
    path("current", CurrentView.as_view(), name="current_goals"),
    path("archive", ArchiveView.as_view(), name="archive_goals"),
    path("create", CreateView.as_view(), name="create_goal"),
    path("update/<uuid:pk>/", UpdateView.as_view(), name="update_goal"),
    path("delete/<uuid:pk>/<path:next>", DeleteView.as_view(), name="delete_goal"),
]
