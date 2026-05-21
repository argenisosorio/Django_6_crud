"""
Tareas para la app Person.

Esta aplicación es responsable de gestionar los registros de personas.
"""

# Importa el decorador task desde django_tasks para registrar tareas
from django_tasks import task

# Importa la función send_mail desde django.core.mail para enviar correos electrónicos
from django.core.mail import send_mail

# Importa el módulo time para agregar retrasos
import time

# Importa el objeto settings desde django.conf para acceder a la configuración de la aplicación
from django.conf import settings

@task()
def send_welcome_email(person_id, person_name, person_email):
    """
    Envía un correo electrónico de bienvenida a la persona.

    Args:
        person_id (int): El ID de la persona.
        person_name (str): El nombre de la persona.
        person_email (str): El correo electrónico de la persona.

    Returns:
        str: Un mensaje indicando que el correo electrónico fue enviado
            exitosamente.
    """
    # Asunto del correo electrónico
    subject = 'Bienvenido a Django 6 Crud'
    # Mensaje del correo electrónico
    message = f'Hola {person_name},\n\nBienvenido a Django 6 Crud.'
    # Remitente del correo electrónico
    from_email = settings.EMAIL_HOST_USER
    # Lista de destinatarios del correo electrónico
    recipient_list = [person_email]

    # Envía el correo electrónico
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
    
    # Retorna el resultado de la tarea
    return f"Email sent successfully to {person_email}";
