from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    """
    Formulario para el registro de usuario en el sistema.
    """
    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "is_active",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User

        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "is_active",
        )