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
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255, default="")
    # email = models.CharField(unique=True, max_length=255)
    email_verified_at = models.DateTimeField(blank=True, null=True)
    # password = models.CharField(max_length=255)
    role = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        db_comment="Tipo de role:\n ADM = Administrador,\n SUP = Supervisor,\n OPD = Operador de donantes,\n OPS = Operador de solicitudes,\n PIN = Personal de inmunología,\n CHO = Coordinador hospitalario\n USR = Usuario,",
    )
    remember_token = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        db_comment="Fecha y hora en la que el registro fue eliminado",
    )

    class Meta:
        # managed = False
        db_table = "users"
