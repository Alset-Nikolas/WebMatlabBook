from django.contrib import admin
from django.urls import include, path

from .views import (
    CreateTaskView,
    ListTaskView,
    DetailTaskView,
    CheckTaskView,
    UpdateTaskView,
    DeleteTaskView,
)

app_name = "tasks"
urlpatterns = [
    path(
        "tasks/create/",
        CreateTaskView.as_view(),
        name="task_create",
    ),
    path(
        "tasks/<slug:section_slug>/",
        ListTaskView.as_view(),
        name="task_list",
    ),
    path(
        "tasks/<slug:task_slug>/update/",
        UpdateTaskView.as_view(),
        name="task_update",
    ),
    path(
        "tasks/<slug:task_slug>/delete/",
        DeleteTaskView.as_view(),
        name="task_delete",
    ),
    path(
        "tasks/info/<slug:task_slug>/",
        DetailTaskView.as_view(),
        name="task_detail",
    ),
    path(
        "task/check/<slug:task_slug>/",
        CheckTaskView.as_view(),
        name="task_check",
    ),
]
