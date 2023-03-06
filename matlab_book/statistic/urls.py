from django.contrib import admin
from django.urls import include, path
from .views import StatisticUserView, StatisticUserUpdateView

app_name = "statistics"

urlpatterns = [
    path(
        "statistics/<slug:discipline_slug>/",
        StatisticUserView.as_view(),
        name="statistics_list",
    ),
    path(
        "statistics/user/<slug:user__username>/<slug:task_slug>/",
        StatisticUserUpdateView.as_view(),
        name="statistics_update",
    ),
]
