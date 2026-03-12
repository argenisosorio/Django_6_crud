from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


"""
Método para validar el tamaño del archivo, se puede usar en cualquier campo de
tipo FileField o ImageField
"""
def validator_file_size_limit(value):
        """Validación de limite de tamaño del archivo

        Parameters
        ----------
        value : File
            Archivo

        Raises
        ------
        ValidationError
            Error de validacion al superar el limite de peso del archivo
        """
        limit = 2 * 1024 * 1024
        if value.size > limit:
            raise ValidationError('File too large. Size should not exceed 2 MiB.')

"""
Método para generar una ruta nueva para el archivo de imagen del modelo, se
puede usar en cualquier campo de tipo ImageField
"""
def get_media_folder_name(instance, file_name='dni'):
    """
    Generar una ruta nueva para el archivo de imagen del modelo

    Parameters
    ----------
    instance : Person
        instancia del modelo
    file_name : str, optional
        nombre del archivo con la extension, by default 'dni'

    Returns
    -------
    str
        ruta nueva del archivo de imagen
    """
    return f'dni/{instance.name}/{file_name}'


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

    # Campo Documento con validación de tamaño y extensión
    document = models.FileField(
        default="",
        upload_to="files/",
        validators=[
            FileExtensionValidator(
                ['pdf', 'docx', 'odt']
            ),
            validator_file_size_limit
        ],
    )

    # Campo Documento de identidad con validación de tamaño y extensión
    dni_file = models.ImageField(
        default="",
        upload_to=get_media_folder_name,
        validators=[
            FileExtensionValidator(
                ['jpg', 'jpeg', 'png', 'avif']
            ),
            validator_file_size_limit
        ],
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
