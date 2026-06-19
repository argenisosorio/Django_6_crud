from django.db import models
from django.conf import settings


class FuelStorage(models.Model):
    """
    Modelo para gestionar el almacenamiento de combustible.
    """
    # Capacidad máxima.
    maximum_capacity = models.IntegerField()

    # Cantidad actual.
    current_amount = models.IntegerField()

    def __str__(self) -> str:
        """
        Devuelve la cantidad actual de combustible como una representación de cadena.
        """
        return f"Current Amount: {self.current_amount}"
