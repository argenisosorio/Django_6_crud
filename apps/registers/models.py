from django.db import models
from django.conf import settings


class Register(models.Model):
    # Partido 1
    marcador_local_game_1 = models.CharField(max_length=10)
    marcador_visitante_game_1 = models.CharField(max_length=10)
    puntos_game_1 = models.CharField(max_length=10, null=True, blank=True)
    # Partido 2
    marcador_local_game_2 = models.CharField(max_length=10)
    marcador_visitante_game_2 = models.CharField(max_length=10)
    puntos_game_2 = models.CharField(max_length=10, null=True, blank=True)
    # Partido 3
    marcador_local_game_3 = models.CharField(max_length=10)
    marcador_visitante_game_3 = models.CharField(max_length=10)
    puntos_game_3 = models.CharField(max_length=10, null=True, blank=True)
    # Partido 4
    marcador_local_game_4 = models.CharField(max_length=10)
    marcador_visitante_game_4 = models.CharField(max_length=10)
    puntos_game_4 = models.CharField(max_length=10, null=True, blank=True)
    # Partido 5
    marcador_local_game_5 = models.CharField(max_length=10)
    marcador_visitante_game_5 = models.CharField(max_length=10)
    puntos_game_5 = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Nuevo campo para almacenar quién hizo el registro
    usuario_registro = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        # Related name para acceder a los registros desde el usuario, por
        # ejemplo: user.registros_realizados.all()
        related_name='registros_realizados',
        # verbose_name para que se muestre mejor en el admin
        verbose_name="Registrado por:"
    )

    def __str__(self):
        return self.result_game_1
