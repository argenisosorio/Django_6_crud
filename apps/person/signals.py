from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Person
from .tasks import send_welcome_email

@receiver(post_save, sender=Person)
def trigger_welcome_email(sender, instance, created, **kwargs):
    """
    Envía un correo electrónico de bienvenida al crear una persona.
    """
    if created:
        send_welcome_email.enqueue(instance.id, instance.name, instance.email)
        

