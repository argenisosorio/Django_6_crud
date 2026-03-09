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
    # Sobrescribimos email para que sea obligatorio y único si es necesario
    email = models.EmailField(unique=True, max_length=255)

    name = models.CharField(max_length=255, default="", blank=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    # Definición de Roles usando Choices de Django
    ROLE_CHOICES = [
        ('ADM', 'Administrador'),
        ('SUP', 'Supervisor'),
        ('OPD', 'Operador de donantes'),
        ('OPS', 'Operador de solicitudes'),
        ('PIN', 'Personal de inmunología'),
        ('CHO', 'Coordinador hospitalario'),
        ('USR', 'Usuario'),
    ]

    role = models.CharField(
        max_length=255, # Suficiente para los códigos de 3 letras
        choices=ROLE_CHOICES,
        default='USR',
        blank=True,
        null=True,
        help_text="Rol asignado al usuario dentro del sistema"
    )

    remember_token = models.CharField(max_length=100, blank=True, null=True)

    # Timestamps automatizados al estilo Django
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    deleted_at = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Fecha y hora en la que el registro fue eliminado (Soft Delete)"
    )

    class Meta:
        db_table = "users"
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self) -> str:
        return f"{self.username} ({self.get_role_display()})"
