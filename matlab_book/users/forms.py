from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput, CharField
from django.contrib.auth.forms import AuthenticationForm


class RegisterUserForm(UserCreationForm):
    username = CharField(
        label="Логин",
        widget=TextInput(
            attrs={
                "class": "register__form__input",
            }
        ),
    )
    password1 = CharField(
        label="Пароль",
        widget=PasswordInput(
            attrs={
                "class": "register__form__input",
            }
        ),
    )
    password2 = CharField(
        label="Повтор пароля",
        widget=PasswordInput(
            attrs={
                "class": "register__form__input",
            }
        ),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class LoginUserForm(AuthenticationForm):
    username = CharField(
        label="Логин",
        widget=TextInput(
            attrs={
                "class": "register__form__input",
            }
        ),
    )
    password = CharField(
        label="Пароль",
        widget=PasswordInput(
            attrs={
                "class": "register__form__input",
            }
        ),
    )

    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )
