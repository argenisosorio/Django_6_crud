from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import User

"""
Formularios para crear y actualizar el modelo "Usuario" personalizado.

Este módulo proporciona dos clases de formulario que encapsulan los formularios
de usuario integrados de Django y los dirigen al modelo "Usuario" del proyecto.
Exhiben los campos de usuario comunes y el campo "rol" específico de la
aplicación.
"""


class CustomUserCreationForm(UserCreationForm):
    """
    Formulario utilizado para crear nuevas instancias de User.

    Utiliza el comportamiento UserCreationForm de Django, pero se dirige al
    modelo User personalizado del proyecto y expone los campos username,
    email, first_name, last_name y role.
    """

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "role")


class CustomUserChangeForm(forms.ModelForm):
    """
    Formulario utilizado para editar instancias de User existentes.

    Contiene el UserChangeForm de Django para el modelo User del proyecto y
    expone el mismo conjunto de campos editables que el formulario de creación.
    """

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "role")
