from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator

class Person(models.Model):
    """
    Represents a person in the system.
    
    This model stores basic information about individuals including their name,
    email, age, and timestamps for record creation and updates.
    """

    name = models.CharField(
        max_length=5,
        validators=[RegexValidator(r'\d', inverse_match=True, message='El campo nombre no permite números.')],
        error_messages={
            'max_length': 'El campo nombre no puede tener más de 5 caracteres.',
            'blank': 'El campo nombre es requerido.',
            'required': 'El campo nombre es requerido.',
        }
    )

    email = models.EmailField(
        max_length=254,
        error_messages={
            'invalid': 'El campo email no es una dirección de correo electrónico válida.',
            'blank': 'El campo email es requerido.',
            'required': 'El campo email es requerido.',
        }
    )

    age = models.PositiveIntegerField(
        validators=[MaxValueValidator(120, message='El campo edad no permite más de 120 años.')],
        error_messages={
            'invalid': 'El campo edad solo permite números enteros válidos .',
            'blank': 'El campo edad es requerido.',
            'required': 'El campo edad es requerido.',
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
