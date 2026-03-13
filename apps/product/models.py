from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    """
    Represents a product in the system.
    """

    name = models.CharField(
        max_length=100,
        error_messages={
            'max_length': 'Máximo 100 caracteres.',
            'blank': 'Este campo es requerido.',
            'required': 'Este campo es requerido.',
            'null': 'Este campo es requerido.',
        }
    )
    price = models.PositiveIntegerField(
        validators=[MinValueValidator(0, message='No se permiten números negativos.')],
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
        String representation of the Product model.
        
        Returns:
            str: The product's name for easy identification in admin and queries.
        """
        return self.name
