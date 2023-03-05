from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
from .forms import DisciplineForm
from .models import Disciplines
import typing as t
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

# Create your views here.


class CreateDisciplinesView(CreateView):
    form_class = DisciplineForm
    template_name = "disciplines/create.html"


class DetailDisciplineView(DetailView):
    model = Disciplines
    template_name = "disciplines/detail.html"
    context_object_name = "discipline"

    def get_object(self):
        slug = self.kwargs.get("discipline_slug", "")
        return get_object_or_404(Disciplines, slug=slug)


class UpdateDisciplineView(UpdateView):
    model = Disciplines
    template_name = "disciplines/update.html"
    form_class = DisciplineForm
    context_object_name = "discipline"

    def get_object(self):
        slug = self.kwargs.get("discipline_slug", "")
        return get_object_or_404(Disciplines, slug=slug)


class DisciplineDeleteView(DeleteView):
    model = Disciplines
    template_name = "disciplines/delete.html"
    context_object_name = "discipline"
    success_url = reverse_lazy("disciplines:disciplines_list")

    def get_object(self):
        slug = self.kwargs.get("discipline_slug", "")
        return get_object_or_404(Disciplines, slug=slug)


class DisciplinesView(ListView):
    model = Disciplines
    context_object_name = "disciplines"
    template_name = "disciplines/index.html"

    def get_context_data(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self) -> t.Any:
        return Disciplines.objects.all()
