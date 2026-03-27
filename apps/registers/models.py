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


class Parroquia(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True,
        verbose_name="Código de la parroquia"
    )
    nombre = models.CharField(
        max_length=100,
        verbose_name="Nombre de la parroquia"
    )
    municipio = models.ForeignKey(
        Municipio,
        on_delete=models.CASCADE,  # Si se elimina un municipio, se eliminan sus parroquias
        related_name='parroquias',  # Permite acceder a todas las parroquias de un municipio: municipio.parroquias.all()
        verbose_name="Municipio"
    )

    class Meta:
        verbose_name = "Parroquia"
        verbose_name_plural = "Parroquias"
        ordering = ['municipio__nombre', 'nombre']  # Ordena primero por municipio, luego por nombre
        unique_together = ['codigo', 'municipio']  # El código es único dentro de cada municipio

    def __str__(self):
        #return f"{self.nombre} - {self.municipio.nombre}"
        return f"{self.nombre}"


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
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='registros',
        verbose_name="Municipio"
    )

    # Nuevo campo parroquia
    parroquia = models.ForeignKey(
        Parroquia,
        on_delete=models.SET_NULL,  # Si se elimina una parroquia, se pone NULL
        null=True,
        blank=True,
        related_name='registros',  # Permite acceder a todos los registros de una parroquia: parroquia.registros.all()
        verbose_name="Parroquia"
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
        on_delete=models.CASCADE,
        related_name='registros_realizados',
        verbose_name="Registrado por:"
    )

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
