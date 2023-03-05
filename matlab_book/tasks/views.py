from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)
import typing as t
from .forms import SectionTaskForm, CheckMatlabFileForm
from .models import SectionTasks
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404, redirect
import typing as t
from oct2py import Oct2Py, octave
import os
from django.conf import settings
import pkgutil
from permissions.permissions import SuperUserPermission, UserAuthPermission
import os
from multiprocessing import Process
from datetime import datetime, timedelta
import time
import signal
from threading import Thread
from sections.models import Sections


class CreateTaskView(SuperUserPermission, CreateView):
    form_class = SectionTaskForm
    template_name = "tasks/create.html"

    def get_success_url(self) -> str:
        return reverse(
            "tasks:task_list",
            kwargs={"section_slug": self.object.section.slug},
        )


class ListTaskView(ListView):
    model = SectionTaskForm
    template_name = "tasks/index.html"
    context_object_name = "tasks"

    def get_queryset(self) -> t.Any:
        slug = self.kwargs.get("section_slug", "")
        return SectionTasks.objects.filter(section__slug=slug).all()

    def get_context_data(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:

        context = super().get_context_data(**kwargs)
        context["section"] = Sections.objects.get(
            slug=self.kwargs.get("section_slug", "")
        )
        return context


class DetailTaskView(DetailView):
    model = SectionTasks
    template_name = "tasks/detail.html"
    context_object_name = "task"

    def get_object(self):
        slug = self.kwargs.get("task_slug", "")
        return get_object_or_404(SectionTasks, slug=slug)

    def get_context_data(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        image = str(obj.image)
        context["flag"] = False
        context["img"] = image[len("staticfiles/") :] if image else None
        return context


class DeleteTaskView(SuperUserPermission, DeleteView):
    model = SectionTasks
    template_name = "tasks/delete.html"
    context_object_name = "task"
    success_url = reverse_lazy("sections:sections_list")

    def get_object(self):
        slug = self.kwargs.get("task_slug", "")
        return get_object_or_404(SectionTasks, slug=slug)

    def get_success_url(self) -> str:
        return reverse(
            "tasks:task_list",
            kwargs={"section_slug": self.object.section.slug},
        )


class UpdateTaskView(SuperUserPermission, UpdateView):
    model = SectionTasks
    template_name = "tasks/update.html"
    form_class = SectionTaskForm
    context_object_name = "task"

    def get_object(self):
        slug = self.kwargs.get("task_slug", "")
        return get_object_or_404(SectionTasks, slug=slug)

    def get_context_data(self, **kwargs: t.Any) -> t.Dict[str, t.Any]:
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context["section_slug"] = obj.section.slug
        return context

    def get_success_url(self):
        return reverse(
            "tasks:task_detail", kwargs={"task_slug": self.object.slug}
        )

    def form_valid(self, form: SectionTaskForm):
        x = form.save()
        return super().form_valid(form)


class CheckTaskView(UserAuthPermission, View):
    def handle_uploaded_file(self, file):
        path_dir_user = os.path.join(
            settings.BASE_DIR,
            "mediafiles",
            "matlab_scripts",
            str(self.request.user.id),
        )
        if not os.path.exists(path_dir_user):
            os.makedirs(path_dir_user)
            octave.addpath(path_dir_user)
        file_path = os.path.join(path_dir_user, "test.m")
        with open(file_path, "wb") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        return file_path

    def add_models_test(self, task):
        path_test = settings.BASE_DIR_TEST_MATLAB_SCRIPTS
        print("path_test", path_test)
        for module_finder, name, ispkg in pkgutil.iter_modules(
            path=[str(path_test)]
        ):
            file_name = str(task.path_test).split("/")[-1]
            print("file_name", file_name)
            if file_name and name == file_name[:-3]:
                mod = module_finder.find_module(name).load_module(name)
                return mod.generate

    def go_matlab_scripts(
        self, teacher_script_path, student_script_path, args, context
    ):
        print("context", context)
        context["args"] = args
        context["admin_res"] = octave.feval(
            teacher_script_path,
            *args,
        )
        context["student_res"] = octave.feval(
            student_script_path,
            *args,
        )
        print("context", context)

    def check_matlab(self, file_student_file, task):
        generation_function = self.add_models_test(task)
        context = dict()
        N = 100
        context["q_tests_all"] = N
        context["q_tests"] = N
        n = 0
        if not generation_function:
            context["err_msg"] = "Тестов пока нету!"
            return True, context

        try:
            octave.timeout = 0.1

            for n in range(N):

                args = generation_function()
                self.go_matlab_scripts(
                    os.path.join(settings.MEDIA_ROOT, str(task.path_script)),
                    str(file_student_file),
                    args,
                    context,
                )
                if str(context["admin_res"]) != str(context["student_res"]):
                    context["err_msg"] = "Ответ не совпал"
                    context["q_tests"] = n
                    return False, context
                else:
                    print("admin_res", context["admin_res"])
                    print("student_res", context["student_res"])
            return True, context

        except BaseException as err:
            print(err)
            context["q_tests"] = n
            context["student_res"] = str(err)
            context["err_msg"] = "Что-то пошло не так"
        return False, context

    def post(self, request, *args, **kwargs):
        task: SectionTasks = get_object_or_404(
            SectionTasks, slug=self.kwargs.get("task_slug", "")
        )
        form = CheckMatlabFileForm(request.POST, request.FILES)
        context = {"task": task, "error_text": None, "flag": False}
        test_context = {}
        if form.is_valid():
            path_student_file = self.handle_uploaded_file(
                file=request.FILES.get("file")
            )
            flag, test_context = self.check_matlab(path_student_file, task)

            if flag:
                test_context["flag"] = True
                return render(
                    request,
                    "tasks/detail.html",
                    context={**context, **test_context},
                )
        context["error_text"] = "Что-то не так с файлом."
        return render(
            request,
            "tasks/detail.html",
            context={**context, **test_context},
        )

    def get(self, request, *args, **kwargs):
        slug = self.kwargs.get("task_slug", "")
        return redirect("tasks:task_detail", task_slug=slug)
