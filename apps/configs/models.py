from django.db import models


class Config(models.Model):
    # False significa que está permitido, True que está deshabilitado
    disable_update_quiniela = models.BooleanField(
        default=False, 
        verbose_name="Deshabilitar actualización de quinielas"
    )
    disable_registration = models.BooleanField(
        default=False, 
        verbose_name="Deshabilitar nuevos registros en el sistema"
    )
    disable_view_register = models.BooleanField(
        default=False,
        verbose_name="Deshabilitar visualización de detalle de un registro"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración"
        verbose_name_plural = "Configuraciones"

    def __str__(self):
        return f"Configuración del sistema ({self.updated_at.strftime('%Y-%m-%d %H:%M')})"
