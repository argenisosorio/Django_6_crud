from django_tasks import task
from django.core.mail import send_mail
import time
from django.conf import settings

@task()
def send_welcome_email(person_id, person_name, person_email):
    """
    Envía un correo electrónico de bienvenida a la persona.
    """

    subject = 'Bienvenido a Django 6 Crud'
    message = f'Hola {person_name},\n\nBienvenido a Django 6 Crud.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [person_email]
    
    send_mail(
        subject,
        message,
        from_email,
        recipient_list,
        fail_silently=False,
    )
    
    return f"Email sent successfully to {person_email}";
