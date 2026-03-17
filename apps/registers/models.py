from django.db import models

class Register(models.Model):
    # Opciones para los campos Select
    PARROQUIAS = [
        ("Antonio Spinetti Dini", "Antonio Spinetti Dini"),
        ("Arias", "Arias"),
        ("Caracciolo Parra Pérez", "Caracciolo Parra Pérez"),
        ("Domingo Peña", "Domingo Peña"),
        ("El Llano", "El Llano"),
        ("El Sagrario", "El Sagrario"),
        ("Gonzalo Picón Febres", "Gonzalo Picón Febres"),
        ("Jacinto Plaza", "Jacinto Plaza"),
        ("Lasso de la Vega", "Lasso de la Vega"),
        ("Juan Rodríguez Suárez", "Juan Rodríguez Suárez"),
        ("Mariano Picón Salas", "Mariano Picón Salas"),
        ("Milla", "Milla"),
        ("Osuna Rodríguez", "Osuna Rodríguez"),
    ]

    TAMANOS = [
        ("Pequeña", "Pequeña"),
        ("Mediana", "Mediana"),
        ("Grande", "Grande"),
    ]

    # Campos de Identificación y Contacto
    nombres = models.CharField(max_length=150)
    apellidos = models.CharField(max_length=150)
    cedula = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    parroquia = models.CharField(max_length=100, choices=PARROQUIAS)

    # Campos de Logística y Trámite
    fecha_registro = models.DateField()
    fecha_despacho = models.DateField(null=True, blank=True)
    retirado_por = models.CharField(max_length=255, null=True, blank=True)
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

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
