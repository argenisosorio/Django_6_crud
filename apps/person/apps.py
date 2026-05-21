"""
Configuración para la aplicación Person.

Esta aplicación es responsable de gestionar los registros de personas.
"""

from django.apps import AppConfig


class PersonConfig(AppConfig):
    """
    Configuración para la aplicación Person.

    Attributes:
        default_auto_field (str): El campo auto para usar en los modelos.
        name (str): El nombre de la app.

    Methods:
        ready(self): Configura las señales de la app al iniciar.

    Signals:
        - post_save: Envía un correo electrónico al usuario después de crear una nueva persona.
        - post_delete: Envía un correo electrónico al usuario después de eliminar una persona.
    """
    # Campo auto predeterminado para usar en los modelos.
    default_auto_field = 'django.db.models.BigAutoField'

    # El nombre de la app.
    name = 'apps.person'

    def ready(self):
        """
        Configuración de las señales de la app.
        """
        import apps.person.signals
