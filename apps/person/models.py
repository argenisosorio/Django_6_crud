from django.db import models
from django.core.validators import RegexValidator

class Person(models.Model):
    """
    Represents a person in the system.
    
    This model stores basic information about individuals including their name,
    email, age, and timestamps for record creation and updates.
    """

    # Personal Information Fields
    name = models.CharField(
        max_length=5,
        validators=[RegexValidator(r'\d', inverse_match=True, message='No se permiten números.')],
        error_messages={
            'max_length': 'Máximo 5 caracteres.',
            'blank': 'Este campo es requerido.',
            'required': 'Este campo es requerido.',
        }
    )

    email = models.EmailField()
    age = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Person model.
        
        Returns:
            str: The person's name for easy identification in admin and queries.
        """
        return self.name