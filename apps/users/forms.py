from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
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


class UpdateUserPasswordForm(SetPasswordForm):
    """
    Formulario para que el administrador actualice la contraseña de un usuario.
    """
    # SetPasswordForm ya trae los campos 'new_password1' y 'new_password2'
    # Si quieres personalizar el widget o etiquetas, puedes redefinirlos aquí,
    # pero no necesitas un 'class Meta'.
    pass
