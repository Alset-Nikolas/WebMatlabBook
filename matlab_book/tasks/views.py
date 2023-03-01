from django.shortcuts import render

# Create your views here.
from .models import SectionTasks
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
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404, redirect
import typing as t
from oct2py import Oct2Py, octave
import os
from django.conf import settings
import staticfiles.tasks.tests as matlab_tests
import pkgutil


class CreateTaskView(CreateView):
    form_class = SectionTaskForm
    template_name = "tasks/create.html"


class ListTaskView(ListView):
    model = SectionTaskForm
    template_name = "tasks/index.html"
    context_object_name = "tasks"

    def get_queryset(self) -> t.Any:
        slug = self.kwargs.get("section_slug", "")
        return SectionTasks.objects.filter(section__slug=slug).all()


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
        context["img"] = image[len("staticfiles/") :] if image else None
        return context


class CheckTaskView(View):
    def handle_uploaded_file(self, file):
        path_dir_user = os.path.join(
            settings.BASE_DIR, "staticfiles", "matlab_scripts", "1"
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
        for module_finder, name, ispkg in pkgutil.iter_modules(
            path=[str(path_test)]
        ):
            file_name = str(task.path_test).split("/")[-1]
            if file_name and name == file_name[:-3]:
                mod = module_finder.find_module(name).load_module(name)
                return mod.generate

    def check_matlab(self, file_student_file, task):
        generation_function = self.add_models_test(task)
        context = dict()
        if not generation_function:
            context["err_msg"] = "Тестов пока нету!"
            return True, context

        try:
            for _ in range(10):
                args = generation_function()
                context["args"] = args
                context["admin_res"] = octave.feval(
                    str(task.path_script), *args
                )
                context["student_res"] = octave.feval(
                    str(file_student_file), *args
                )
                if str(context["admin_res"]) != str(context["student_res"]):
                    context["err_msg"] = "Ответ не совпал"
                    return False, context
            return True, context

        except BaseException as err:
            print(err)
            context["err_msg"] = "Что-то пошло не так"
        return False, context

    def post(self, request, *args, **kwargs):
        task: SectionTasks = get_object_or_404(
            SectionTasks, slug=self.kwargs.get("task_slug", "")
        )
        form = CheckMatlabFileForm(request.POST, request.FILES)
        context = {"task": task, "error_text": "Все Ок", "flag": False}
        test_context = {}
        if form.is_valid():
            # octave.feval("/matlab_sctepts/myScript", 7)
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
        print({**context, **test_context})
        return render(
            request,
            "tasks/detail.html",
            context={**context, **test_context},
        )
