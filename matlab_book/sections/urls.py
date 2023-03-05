from django.contrib import admin
from django.urls import include, path
from .views import (
    CreateSectionsView,
    SectionsView,
    DetailSectionView,
    UpdateSectionView,
    SectionDeleteView,
)

app_name = "sections"

urlpatterns = [
    path(
        "sections/create/",
        CreateSectionsView.as_view(),
        name="section_create",
    ),
    path(
        "sections/<slug:section_slug>/",
        DetailSectionView.as_view(),
        name="section_detail",
    ),
    path(
        "sections/<slug:section_slug>/update/",
        UpdateSectionView.as_view(),
        name="section_update",
    ),
    path(
        "sections/<slug:section_slug>/delete/",
        SectionDeleteView.as_view(),
        name="section_delete",
    ),
    path(
        "sections/<slug_discipline>",
        SectionsView.as_view(),
        name="sections_list",
    ),
]
