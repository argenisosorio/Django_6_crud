from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
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
            "nickname",
        )


class CustomUserChangeForm(forms.ModelForm):
    """
    Formulario para actualizar datos de un usuario registrado.
    """
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "nickname",
        )


class ProfileForm(forms.ModelForm):
    """
    Formulario para la actualización de datos del perfil
    """
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "nickname",
        )
