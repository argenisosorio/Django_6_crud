"""
Modelo para la aplicación Person.

Esta aplicación es responsable de gestionar los registros de personas.
"""

from django.db import models


class Person(models.Model):
    """
    Representa una persona en el sistema.
    
    Este modelo almacena información básica sobre las personas, incluyendo su
    nombre, correo electrónico, edad y marcas de tiempo para la creación y
    actualización de registros.

    Attributes:
        name (str): El nombre de la persona.
        email (str): El correo electrónico de la persona.
        age (int): La edad de la persona.
        created_at (datetime): La fecha y hora de creación del registro.
        updated_at (datetime): La fecha y hora de actualización del registro.

    Methods:
        __str__(self): Retorna una representación en cadena del modelo Persona.

    Signals:
        - post_save: Envía un correo electrónico al usuario después de crear
            una nueva persona.
        - post_delete: Envía un correo electrónico al usuario después de eliminar
            una persona.
    """

    # Campos de información personal
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Representación en cadena del modelo Persona.
        
        Returns:
            str: El nombre de la persona para una fácil identificación en el
                administrador y consultas.
        """
        # Retorna el nombre de la persona para una fácil identificación en el
        # administrador y consultas.
        return self.name
