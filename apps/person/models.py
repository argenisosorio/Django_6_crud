from django.db import models
from django.core.validators import FileExtensionValidator


class Person(models.Model):
    """
    Represents a person in the system.
    
    This model stores basic information about individuals including their name,
    email, age, and timestamps for record creation and updates.
    """

    # Personal Information Fields
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.PositiveIntegerField()

    # Campo Documento DNI.
    dni_file = models.FileField(
        upload_to='',
        blank=True,
        null=True,
        default="",
        validators=[
            FileExtensionValidator(allowed_extensions=[
                'pdf',
                'odt'
            ])
        ],
        help_text="Solo se permiten archivos PDF, ODT."
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
