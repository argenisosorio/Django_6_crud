from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
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
            "favorite_team",
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        nickname = cleaned_data.get("nickname")

        # Validación: username no puede ser igual a nickname
        if username and nickname and username.lower() == nickname.lower():
            raise ValidationError({
                "nickname": "El apodo en la Quiniela no puede ser igual al nombre de usuario.",
                "username": "El nombre de usuario no puede ser igual al apodo en la Quiniela."
            })

        return cleaned_data


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
            "favorite_team",
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        nickname = cleaned_data.get("nickname")

        # Validación: username no puede ser igual a nickname
        if username and nickname and username.lower() == nickname.lower():
            raise ValidationError({
                "nickname": "El apodo en la Quiniela no puede ser igual al nombre de usuario.",
                "username": "El nombre de usuario no puede ser igual al apodo en la Quiniela."
            })

        return cleaned_data


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
            "favorite_team",
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("username")
        nickname = cleaned_data.get("nickname")

        # Validación: username no puede ser igual a nickname
        if username and nickname and username.lower() == nickname.lower():
            raise ValidationError({
                "nickname": "El apodo en la Quiniela no puede ser igual al nombre de usuario.",
                "username": "El nombre de usuario no puede ser igual al apodo en la Quiniela."
            })

        return cleaned_data
