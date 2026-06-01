import re
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from .models import User


def validar_campos_perfil(cleaned_data):
    """
    Función auxiliar para centralizar la validación de campos duplicados.
    """
    errors = {}
    username = cleaned_data.get("username")
    first_name = cleaned_data.get("first_name")
    last_name = cleaned_data.get("last_name")
    nickname = cleaned_data.get("nickname")
    phone = cleaned_data.get("phone")

    if nickname:
        nickname_lower = nickname.lower()

        # 1. Validación: username vs nickname
        if username and username.lower() == nickname_lower:
            errors["username"] = "El nombre de usuario no puede ser igual al apodo."
            errors["nickname"] = "El apodo no puede ser igual al nombre de usuario."

        # 2. Validación: first_name vs nickname
        if first_name and first_name.lower() == nickname_lower:
            errors["first_name"] = "El nombre no puede ser igual al apodo."
            if "nickname" not in errors:
                errors["nickname"] = "El apodo no puede ser igual a tu nombre."

        # 3. Validación: last_name vs nickname
        if last_name and last_name.lower() == nickname_lower:
            errors["last_name"] = "El apellido no puede ser igual al apodo."
            if "nickname" not in errors:
                errors["nickname"] = "El apodo no puede ser igual a tu apellido."

    if phone:
        # Expresión regular que permite: números, espacios, guiones (-) y el signo (+)
        # ^[0-9\s+-]+$ asegura que todo el string cumpla con estos caracteres de inicio a fin
        formato_valido = re.match(r"^[0-9\s+-]+$", phone)

        if not formato_valido:
            errors["phone"] = "El número de teléfono solo puede contener números, espacios, guiones y el signo '+'."

    if errors:
        raise ValidationError(errors)


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
            "phone",
        )

    """
    La validación de campos duplicados se centraliza en la función auxiliar
    `validar_campos_perfil` para evitar la repetición de código en los distintos
    formularios.
    """
    def clean(self):
        cleaned_data = super().clean()
        validar_campos_perfil(cleaned_data)
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
            "phone",
        )

    """
    La validación de campos duplicados se centraliza en la función auxiliar
    `validar_campos_perfil` para evitar la repetición de código en los distintos
    formularios.
    """
    def clean(self):
        cleaned_data = super().clean()
        validar_campos_perfil(cleaned_data)
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
            "phone",
        )

    """
    La validación de campos duplicados se centraliza en la función auxiliar
    `validar_campos_perfil` para evitar la repetición de código en los distintos
    formularios.
    """
    def clean(self):
        cleaned_data = super().clean()
        validar_campos_perfil(cleaned_data)
        return cleaned_data


class UpdateUserActiveForm(forms.ModelForm):
    """
    Formulario para la actualización del campo active del usuario.
    """
    class Meta:
        model = User
        fields = (
            "is_active",
        )


class UpdatePasswordForm(forms.ModelForm):
    """
    Formulario para actualizar la contraseña de un usuario registrado.
    """
    class Meta:
        model = User
        fields = (
            "password",
        )
