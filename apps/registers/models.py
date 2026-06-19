from django.db import models
from django.conf import settings


class FuelStorage(models.Model):
    """
    Modelo para gestionar el almacenamiento de combustible.
    """
    # Capacidad máxima.
    maximum_capacity = models.IntegerField(
        default=0,
        verbose_name="Capacidad máxima"
    )

    # Cantidad actual.
    current_amount = models.IntegerField(
        default=0,
        verbose_name="Cantidad actual"
    )

    def __str__(self) -> str:
        """
        Devuelve la cantidad actual de combustible como una representación de cadena.
        """
        return f"Current Amount: {self.current_amount}"


class RegisterFuel(models.Model):
    """
    Modelo para gestionar los movimientos de combustible.
    """
    MOVEMENT_TYPES = [
        ("Entrada", "Entrada"),
        ("Salida", "Salida"),
    ]

    # Fecha de registro del movimiento.
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización del movimiento.
    updated_at = models.DateTimeField(auto_now=True)

    # Tipo de Movimiento (Ingreso/Salida)
    movement_type = models.CharField(
        max_length=20,
        choices=MOVEMENT_TYPES,
        verbose_name="Tipo de movimiento"
    )

    # Cantidad (Litros)
    quantity = models.IntegerField(
        verbose_name="Cantidad (Litros)"
    )

    # Autorizado por.
    authorized_by = models.CharField(
        max_length=100,
        verbose_name="Autorizado por"
    )

    # Observaciones.
    observations = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Observaciones"
    )

    # Que usuario hizo el registro.
    register_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='register_fuel',
        verbose_name="Registrado por"
    )

    def __str__(self) -> str:
        """
        Devuelve la cantidad actual de combustible como una representación de cadena.
        """
        return f"Cantidad en litros: {self.quantity}"
