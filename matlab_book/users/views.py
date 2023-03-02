from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from .forms import RegisterUserForm, LoginUserForm

# Create your views here.
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = "users/login.html"
    success_url = reverse_lazy("sections:sections_list")


class RegisterUserView(CreateView):
    form_class = RegisterUserForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("sections:sections_list")

    def form_valid(self, form: RegisterUserForm):
        user = form.save()
        login(self.request, user)
        return redirect("sections:sections_list")


def logout_user(request):
    logout(request)
    return redirect("sections:sections_list")
