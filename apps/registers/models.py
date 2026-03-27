from django.db import models
from django.conf import settings # Importante para referenciar el User model


class Municipio(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código del municipio"
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre del municipio"
    )
    
    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"
        ordering = ['nombre']
    
    def __str__(self):
        return self.nombre


class Register(models.Model):
    TAMANOS = [
        ("Pequeña", "Pequeña"),
        ("Mediana", "Mediana"),
        ("Grande", "Grande"),
    ]

    # Campos de Identificación y Contacto
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    direccion = models.TextField()
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.SET_NULL,  # Si se elimina un municipio, se pone NULL en lugar de borrar los registros
        null=True,                   # Permite valores NULL (por si hay registros antiguos sin municipio)
        blank=True,                  # Permite dejar el campo vacío en formularios
        related_name='registros',    # Permite acceder a todos los registros de un municipio: municipio.registros.all()
        verbose_name="Municipio"
    )

    # Campos de Logística y Trámite
    fecha_registro = models.DateField()
    fecha_despacho = models.DateField(null=True, blank=True)
    retirado_por = models.CharField(max_length=255)
    retirado_por_ci = models.CharField(max_length=20)
    cantidad = models.PositiveIntegerField(default=1)
    tamano_cilindro = models.CharField(
        max_length=20,
        choices=TAMANOS,
        verbose_name="Tamaño de Cilindro"
    )

    # Campos de Control (Booleanos)
    visitado = models.BooleanField(default=False)
    documentos_completos = models.BooleanField(default=False)

    # Auditoría (Automáticos)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Nuevo campo para almacenar quién hizo el registro
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, # Si se borra el usuario, se borran sus registros (o usa SET_NULL si prefieres conservarlos)
        related_name='registros_realizados',
        verbose_name="Registrado por:"
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
