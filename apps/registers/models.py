from django.db import models
from django.conf import settings
from datetime import date


class Register(models.Model):
    SEXOS = [
        ("M", "M"),
        ("F", "F"),
    ]

    # Datos Personales (Obligatorios para un registro)
    nombres = models.CharField(max_length=150, null=True, blank=True)
    apellidos = models.CharField(max_length=150, null=True, blank=True)
    cedula = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    sexo = models.CharField(
        max_length=1,
        choices=SEXOS,
        verbose_name="Sexo"
    )
    estado_nacimiento=models.CharField(max_length=50, null=True, blank=True)

    # Datos de Localización del Registro (Libro de Actas)
    folio = models.CharField(max_length=15, null=True, blank=True)
    libro = models.CharField(max_length=15, null=True, blank=True)
    numero = models.CharField(max_length=15, null=True, blank=True)
    ano = models.CharField(max_length=15, null=True, blank=True)

    # Datos del Acto
    fecha_bautizo = models.DateField(null=True, blank=True, verbose_name="Fecha de Bautizo")
    padre = models.CharField(max_length=150, null=True, blank=True, verbose_name="Padre")
    madre = models.CharField(max_length=150, null=True, blank=True, verbose_name="Madre")
    padrino_1 = models.CharField(max_length=150, null=True, blank=True, verbose_name="Padrino 1")
    padrino_2 = models.CharField(max_length=150, null=True, blank=True, verbose_name="Padrino 2")
    ministro = models.CharField(max_length=150, null=True, blank=True, verbose_name="Ministro")
    nota_marginal = models.TextField(max_length=1000, null=True, blank=True, verbose_name="Nota Marginal")
    presbitero = models.CharField(max_length=150, null=True, blank=True, verbose_name="Presbitero")

    # Auditoría (Automáticos)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def edad(self):
        """
        Retorna la edad actual en años a partir de la fecha de nacimiento.

        Returns:
            int: Edad en años cumplidos, o None si no hay fecha de nacimiento.
        """
        if self.fecha_nacimiento:
            today = date.today()
            return today.year - self.fecha_nacimiento.year - (
                (today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day)
            )
        return None

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
