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
        ("El Morro", "El Morro"),
        ("Los Nevados", "Los Nevados"),
    ]

    TAMANOS = [
        ("Pequeña", "Pequeña"),
        ("Mediana", "Mediana"),
        ("Grande", "Grande"),
    ]

    # Campos de Identificación y Contacto
    nombres_apellidos = models.CharField(max_length=150)
    puesto_trabajo = models.CharField(max_length=20)
    n_bien_cpu = models.CharField(max_length=20)
    cap_dd = models.CharField(max_length=20)
    serial_dd = models.CharField(max_length=50)
    modelo_dd = models.CharField(max_length=50)
    tipo_dd = models.CharField(max_length=50)
    procesador = models.CharField(max_length=100)
    cant_memorias = models.CharField(max_length=100)
    cap_memorias = models.CharField(max_length=100)
    modelo_memorias = models.CharField(max_length=100)
    max_ram = models.CharField(max_length=100)
    cant_zoc_mem = models.CharField(max_length=100)
    nb_monitor = models.CharField(max_length=100)
    mod_monitor = models.CharField(max_length=100)
    serial_monitor = models.CharField(max_length=100)
    nb_mouse = models.CharField(max_length=100)
    serial_mouse = models.CharField(max_length=100)
    nb_teclado = models.CharField(max_length=100)
    marca_teclado = models.CharField(max_length=100)
    mod_teclado = models.CharField(max_length=100)
    serial_teclado = models.CharField(max_length=100)
    ups = models.CharField(max_length=100)
    marca_ups = models.CharField(max_length=100)
    mod_ups = models.CharField(max_length=100)
    serial_ups = models.CharField(max_length=100)

    # Auditoría (Automáticos)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.cedula}"
