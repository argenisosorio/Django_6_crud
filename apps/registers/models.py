from django.db import models
from django.conf import settings
from datetime import date


class Register(models.Model):
    SEXOS = [
        ("M", "M"),
        ("F", "F"),
    ]

    nombres = models.CharField(max_length=150, null=True, blank=True)
    apellidos = models.CharField(max_length=150, null=True, blank=True)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(
        max_length=1,
        choices=SEXOS,
        verbose_name="Sexo"
    )
    folio = models.CharField(max_length=15, null=True, blank=True)
    libro = models.CharField(max_length=15, null=True, blank=True)
    numero = models.CharField(max_length=15, null=True, blank=True)
    ano = models.CharField(max_length=15, null=True, blank=True)

    # Auditoría (Automáticos)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def edad(self):
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
