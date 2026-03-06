from django.contrib.auth.models import AbstractUser
from django.db import models


"""
Modelo de usuario personalizado para la aplicación users.

Este módulo define un modelo User que extiende el AbstractUser de Django para
incluir un campo role opcional. El modelo mantiene el comportamiento de
autenticación predeterminado, pero permite almacenar un rol de cadena simple
para cada usuario.
"""


class User(AbstractUser):
    """
    Modelo de usuario específico de la aplicación.

    Hereda todos los campos y comportamientos del `AbstractUser` de Django y
    añade un campo role opcional para capturar el rol del usuario dentro de la
    aplicación.
    """

    role = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self) -> str:
        """
        Devuelve el nombre de usuario como una representación de cadena.
        """

        return self.username
