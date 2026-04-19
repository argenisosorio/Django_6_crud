from django.db import models
from django.conf import settings # Importante para referenciar el User model


class Register(models.Model):
    SEXOS = [
        ("M", "M"),
        ("F", "F"),
    ]

    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(
        max_length=1,
        choices=SEXOS,
        verbose_name="Sexo"
    )
    folio = models.CharField(max_length=10)

    # Auditoría (Automáticos)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
