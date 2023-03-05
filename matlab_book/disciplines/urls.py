from django.contrib import admin
from django.urls import include, path
from .views import (
    CreateDisciplinesView,
    DetailDisciplineView,
    UpdateDisciplineView,
    DisciplineDeleteView,
    DisciplinesView,
)

app_name = "disciplines"

urlpatterns = [
    path(
        "disciplines/create/",
        CreateDisciplinesView.as_view(),
        name="discipline_create",
    ),
    path(
        "disciplines/<slug:discipline_slug>/",
        DetailDisciplineView.as_view(),
        name="discipline_detail",
    ),
    path(
        "disciplines/<slug:discipline_slug>/update/",
        UpdateDisciplineView.as_view(),
        name="discipline_update",
    ),
    path(
        "disciplines/<slug:discipline_slug>/delete/",
        DisciplineDeleteView.as_view(),
        name="discipline_delete",
    ),
    path(
        "",
        DisciplinesView.as_view(),
        name="disciplines_list",
    ),
]
