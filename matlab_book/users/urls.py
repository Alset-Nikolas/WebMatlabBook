from django.contrib import admin
from django.urls import path, include
from .views import LoginUserView, RegisterUserView, logout_user

app_name = "users"

urlpatterns = [
    path(
        "accounts/login/",
        LoginUserView.as_view(),
        name="user_login",
    ),
    path(
        "accounts/logout/",
        logout_user,
        name="user_logout",
    ),
    path(
        "accounts/register/",
        RegisterUserView.as_view(),
        name="user_registration",
    ),
]
