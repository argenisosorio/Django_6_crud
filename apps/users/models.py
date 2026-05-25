from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    NATIONS_CHOICES = [
        ("Alemania", "Alemania"),
        ("Arabia Saudita", "Arabia Saudita"),
        ("Argelia", "Argelia"),
        ("Argentina", "Argentina"),
        ("Australia", "Australia"),
        ("Austria", "Austria"),
        ("Bélgica", "Bélgica"),
        ("Bosnia y Herzegovina", "Bosnia y Herzegovina"),
        ("Brasil", "Brasil"),
        ("Cabo Verde", "Cabo Verde"),
        ("Canadá", "Canadá"),
        ("Catar", "Catar"),
        ("Colombia", "Colombia"),
        ("Corea del Sur", "Corea del Sur"),
        ("Costa de Marfil", "Costa de Marfil"),
        ("Croacia", "Croacia"),
        ("Curazao", "Curazao"),
        ("Ecuador", "Ecuador"),
        ("Egipto", "Egipto"),
        ("Escocia", "Escocia"),
        ("España", "España"),
        ("Estados Unidos", "Estados Unidos"),
        ("Francia", "Francia"),
        ("Ghana", "Ghana"),
        ("Haití", "Haití"),
        ("Inglaterra", "Inglaterra"),
        ("Irak", "Irak"),
        ("Irán", "Irán"),
        ("Japón", "Japón"),
        ("Jordania", "Jordania"),
        ("Marruecos", "Marruecos"),
        ("México", "México"),
        ("Noruega", "Noruega"),
        ("Nueva Zelanda", "Nueva Zelanda"),
        ("Países Bajos", "Países Bajos"),
        ("Panamá", "Panamá"),
        ("Paraguay", "Paraguay"),
        ("Portugal", "Portugal"),
        ("R. D. del Congo", "R. D. del Congo"),
        ("República Checa", "República Checa"),
        ("Senegal", "Senegal"),
        ("Sudáfrica", "Sudáfrica"),
        ("Suecia", "Suecia"),
        ("Suiza", "Suiza"),
        ("Túnez", "Túnez"),
        ("Turquía", "Turquía"),
        ("Uruguay", "Uruguay"),
        ("Uzbekistán", "Uzbekistán"),
    ]

    email = models.EmailField(
        unique=True,
        verbose_name="Correo electrónico"
    )
    nickname = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name="Apodo"
    )
    favorite_team = models.CharField(
        max_length=50,
        choices=NATIONS_CHOICES,
        blank=True,
        null=True,
        verbose_name="País favorito"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Código + Teléfono"
    )

    def __str__(self) -> str:
        return self.username
