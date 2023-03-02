from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Sections
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
import typing as t
from .forms import SectionForm
from django.urls import reverse_lazy
from permissions.permissions import SuperUserPermission


class SectionsView(ListView):
    model = Sections
    context_object_name = "sections"
    template_name = "sections/index.html"

    def get_context_data(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self) -> t.Any:
        return Sections.objects.order_by("number_lesson").all()


class CreateSectionsView(SuperUserPermission, CreateView):
    form_class = SectionForm
    template_name = "sections/create_section.html"


class DetailSectionView(DetailView):
    model = Sections
    template_name = "sections/detail.html"
    context_object_name = "section"

    def get_object(self):
        slug = self.kwargs.get("section_slug", "")
        return get_object_or_404(Sections, slug=slug)


class UpdateSectionView(SuperUserPermission, UpdateView):
    model = Sections
    template_name = "sections/update.html"
    form_class = SectionForm
    context_object_name = "section"

    def get_object(self):
        slug = self.kwargs.get("section_slug", "")
        return get_object_or_404(Sections, slug=slug)


class SectionDeleteView(SuperUserPermission, DeleteView):
    model = Sections
    template_name = "sections/delete.html"
    success_url = reverse_lazy("sections:sections_list")
    context_object_name = "section"

    def get_object(self):
        slug = self.kwargs.get("section_slug", "")
        return get_object_or_404(Sections, slug=slug)
