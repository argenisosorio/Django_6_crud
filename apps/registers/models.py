from django.db import models

class Register(models.Model):
    nombres_apellidos = models.CharField(max_length=150, blank=True, null=True)
    puesto_trabajo = models.CharField(max_length=20, blank=True, null=True)
    n_bien_cpu = models.CharField(max_length=20, blank=True, null=True)
    cap_dd = models.CharField(max_length=20, blank=True, null=True)
    serial_dd = models.CharField(max_length=50, blank=True, null=True)
    modelo_dd = models.CharField(max_length=50, blank=True, null=True)
    tipo_dd = models.CharField(max_length=50, blank=True, null=True)
    procesador = models.CharField(max_length=100, blank=True, null=True)
    cant_memorias = models.CharField(max_length=100, blank=True, null=True)
    cap_memorias = models.CharField(max_length=100, blank=True, null=True)
    modelo_memorias = models.CharField(max_length=100, blank=True, null=True)
    max_ram = models.CharField(max_length=100, blank=True, null=True)
    cant_zoc_mem = models.CharField(max_length=100, blank=True, null=True)
    nb_monitor = models.CharField(max_length=100, blank=True, null=True)
    mod_monitor = models.CharField(max_length=100, blank=True, null=True)
    serial_monitor = models.CharField(max_length=100, blank=True, null=True)
    nb_mouse = models.CharField(max_length=100, blank=True, null=True)
    serial_mouse = models.CharField(max_length=100, blank=True, null=True)
    nb_teclado = models.CharField(max_length=100, blank=True, null=True)
    marca_teclado = models.CharField(max_length=100, blank=True, null=True)
    mod_teclado = models.CharField(max_length=100, blank=True, null=True)
    serial_teclado = models.CharField(max_length=100, blank=True, null=True)
    ups = models.CharField(max_length=100, blank=True, null=True)
    marca_ups = models.CharField(max_length=100, blank=True, null=True)
    mod_ups = models.CharField(max_length=100, blank=True, null=True)
    serial_ups = models.CharField(max_length=100, blank=True, null=True)

    # Auditoría (Automáticos)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombres_apellidos}"
