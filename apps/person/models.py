from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator, MinValueValidator, EmailValidator

class Person(models.Model):
    """
    Represents a person in the system.
    
    This model stores basic information about individuals including their name,
    email, age, and timestamps for record creation and updates.
    """

    # Personal Information Fields
    name = models.CharField(
        max_length=100,
        validators=[RegexValidator(r'\d', inverse_match=True, message='No se permiten números.')],
        error_messages={
            'max_length': 'Máximo 100 caracteres.',
            'required': 'Este campo es requerido.',
            'blank': 'Este campo es requerido.',
            'null': 'Este campo es requerido.',
        }
    )
    email = models.EmailField(
        validators=[EmailValidator(message='Formato de correo inválido.')],
        error_messages={
            'invalid': 'Formato de correo inválido.',
            'blank': 'Este campo es requerido.',
            'required': 'Este campo es requerido.',
            'null': 'Este campo es requerido.',
        }
    )
    age = models.PositiveIntegerField(
        validators=[
            MaxValueValidator(100, message='No se permiten números mayores a 100.'),
            MinValueValidator(0, message='No se permiten números negativos.')
        ],
        error_messages={
            'min_value': 'No se permiten números negativos.',
            'blank': 'Este campo es requerido.',
            'required': 'Este campo es requerido.',
            'null': 'Este campo es requerido.',
        }
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Person model.
        
        Returns:
            str: The person's name for easy identification in admin and queries.
        """
        return self.name