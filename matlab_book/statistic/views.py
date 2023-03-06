from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import render, get_object_or_404, redirect
from .models import StatisticsUser
import typing as t
from .forms import SectionTaskForm

# Create your views here.


class StatisticUserView(ListView):
    model = StatisticsUser
    context_object_name = "statistics"
    template_name = "statistics/index.html"
    context_object_name = "statistics"

    def get_context_data(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        context = super().get_context_data(**kwargs)
        stat = self.get_queryset()
        tasks = set()
        last_user = None
        order_tasks = []
        table = []
        for item_stat in stat:
            if item_stat.task not in tasks:
                tasks.add(item_stat.task)
                order_tasks.append(item_stat.task)
            if last_user is None or last_user != item_stat.user:
                last_user = item_stat.user
                table.append([item_stat])
            table[-1].append(item_stat)
        context["order_tasks"] = order_tasks
        context["table"] = table
        context["discipline_slug"] = self.kwargs.get("discipline_slug", "")
        return context

    def get_queryset(self) -> t.Any:
        slug = self.kwargs.get("discipline_slug", "")
        return (
            StatisticsUser.objects.filter(task__section__discipline__slug=slug)
            .order_by("user_id", "task_id")
            .all()
        )


class StatisticUserUpdateView(UpdateView):
    model = StatisticsUser
    form_class = SectionTaskForm
    template_name = "statistics/update.html"
    context_object_name = "statistics"

    def get_object(self):
        user__username = self.kwargs.get("user__username", "")
        task_slug = self.kwargs.get("task_slug", "")
        return get_object_or_404(
            StatisticsUser, user__username=user__username, task__slug=task_slug
        )
