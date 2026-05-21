"""
Señales para la aplicación Person.

Esta aplicación es responsable de gestionar los registros de personas.
"""

# Importa el decorador receiver desde django.dispatch para registrar señales
from django.dispatch import receiver

# Importa la señal post_save desde django.db.models.signals para ser notificado
# después de guardar una instancia de modelo
from django.db.models.signals import post_save

# Importa el modelo Person desde el modelo de la aplicación actual
from .models import Person

# Importa la tarea send_welcome_email desde el módulo de tareas de la aplicación actual
from .tasks import send_welcome_email

# Conecta la señal a la función receptora
# post_save es una señal que se envía después de guardar un modelo, sender es el
# modelo que envió la señal
@receiver(post_save, sender=Person)
def trigger_welcome_email(sender, instance, created, **kwargs):
    """
    Envía un correo electrónico de bienvenida a la persona después de crear un
    nuevo registro.

    Args:
        sender (Model): La clase del modelo que envió la señal.
        instance (Model): La instancia del modelo que se creó.
        created (bool): Si la instancia del modelo se creó en esta llamada.
        **kwargs: Additional keyword arguments.
    """
    # Si la instancia del modelo se creó en esta llamada, envía el correo
    # electrónico de bienvenida,
    if created:
        # Envía la tarea send_welcome_email con el ID, nombre y correo
        # electrónico de la instancia
        send_welcome_email.enqueue(instance.id, instance.name, instance.email)

