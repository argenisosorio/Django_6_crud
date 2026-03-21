from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

class Person(models.Model):
    # Validador: Solo letras y espacios
    solo_letras = RegexValidator(
        regex=r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$',
        message='El campo Nombre solo debe contener letras y espacios.'
    )

    name = models.CharField(
        max_length=100,
        validators=[solo_letras],
        verbose_name="Nombre"
    )

    # EmailField ya valida el formato de correo por defecto en Django
    email = models.EmailField(verbose_name="Correo Electrónico")

    # Validamos que sea entre 0 y 120 años
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(0, message="El campo Edad no puede ser negativo."),
            MaxValueValidator(120, message="El campo Edad no puede ser mayor a 120 años.")
        ],
        verbose_name="Edad"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
