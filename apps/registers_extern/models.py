from django.db import models
from django.conf import settings


class Register_extern(models.Model):
    TIPOS_MOVIMIENTO = [
        ("Entrada", "Entrada"),
        ("Salida", "Salida"),
    ]

    # Fecha de registro.
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización.
    updated_at = models.DateTimeField(auto_now=True)

    # Ente propietario.
    ente_propietario = models.CharField(
        max_length=100,
        verbose_name="Ente propietario"
    )

    # Tipo de Movimiento (Ingreso/Salida)
    tipo_movimiento = models.CharField(
        max_length=20,
        choices=TIPOS_MOVIMIENTO,
        verbose_name="Tipo de movimiento"
    )

    # Cantidad (Litros)
    cantidad_litros = models.CharField(
        max_length=100,
        verbose_name="Cantidad (Litros)"
    )

    # Motivo de uso
    motivo_uso = models.CharField(
        max_length=100,
        verbose_name="Motivo de uso"
    )

    # Autorizado por.
    autorizado_por = models.CharField(
        max_length=100,
        verbose_name="Autorizado por"
    )

    # Recibido/Entregado por.
    rec_entr_por = models.CharField(
        max_length=100,
        verbose_name="Recibido/Entregado por"
    )

    # Observaciones.
    observaciones = models.TextField(
        max_length=500,
        null=True,
        blank=True,
        verbose_name="Observaciones"
    )

    # Que usuario hizo el registro.
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='registros_externos',
        verbose_name="Registrado por"
    )

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.cantidad_litros}L ({self.created_at.strftime('%Y-%m-%d %H:%M')})"
