from django import forms
from django.core.validators import MinLengthValidator, EmailValidator, MinValueValidator, MaxValueValidator
from apps.persons.models.person import Person


"""
Formulario para validar los datos de entrada al actualizar una nueva persona.
Este formulario utiliza los campos definidos en el modelo Person y agrega
validaciones específicas.
"""


class UpdatePersonRequest(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        validators=[MinLengthValidator(2)],
        error_messages={
            'max_length': 'El nombre no puede exceder los 100 caracteres',
            'min_length': 'El nombre debe tener al menos 2 caracteres'
        }
    )

    email = forms.EmailField(
        required=False,
        validators=[EmailValidator()],
        error_messages={
            'invalid': 'Ingrese un correo electrónico válido'
        }
    )
    
    age = forms.IntegerField(
        required=False,
        validators=[
            MinValueValidator(1, message='La edad debe ser mayor a 0'),
            MaxValueValidator(120, message='La edad no puede ser mayor a 120 años')
        ],
        error_messages={
            'invalid': 'Ingrese una edad válida'
        }
    )

    def clean_email(self):
        """Validate that the email is unique (excluding current person)."""
        email = self.cleaned_data.get("email")

        # Si no se proporciona un nuevo correo electrónico, no es necesario validarlo
        if not email:
            return email

        return email

    def clean_name(self):
        """Validate that the name doesn't contain invalid characters."""
        name = self.cleaned_data.get("name")
        
        # Si no se proporciona un nuevo nombre, no es necesario validarlo
        if not name:
            return name

        if not all(c.isalpha() or c.isspace() for c in name):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")

        return name.strip()
