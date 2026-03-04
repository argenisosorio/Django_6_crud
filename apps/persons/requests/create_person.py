from django import forms
from django.core.validators import MinLengthValidator, EmailValidator, MinValueValidator, MaxValueValidator
from apps.persons.models.person import Person

"""
Formulario para validar los datos de entrada al crear una nueva persona. Este
formulario utiliza los campos definidos en el modelo Person y agrega
validaciones específicas
"""


class CreatePersonRequest(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        validators=[MinLengthValidator(2)],
        error_messages={
            'required': 'El nombre es obligatorio',
            'max_length': 'El nombre no puede exceder los 100 caracteres',
            'min_length': 'El nombre debe tener al menos 2 caracteres'
        }
    )

    email = forms.EmailField(
        required=True,
        validators=[EmailValidator()],
        error_messages={
            'required': 'El correo electrónico es obligatorio',
            'invalid': 'Ingrese un correo electrónico válido'
        }
    )

    age = forms.IntegerField(
        required=True,
        validators=[
            MinValueValidator(1, message='La edad debe ser mayor a 0'),
            MaxValueValidator(120, message='La edad no puede ser mayor a 120 años')
        ],
        error_messages={
            'required': 'La edad es obligatoria',
            'invalid': 'Ingrese una edad válida'
        }
    )

    def clean_name(self):
        """
        Validar que el nombre solo contenga letras y espacios.
        """
        name = self.cleaned_data.get("name")
        
        # Validar que el nombre solo contenga letras y espacios
        if not all(c.isalpha() or c.isspace() for c in name):
            raise forms.ValidationError("El nombre solo puede contener letras y espacios.")
        
        return name.strip()

    def clean_email(self):
        """
        Validar que el correo electrónico sea único.
        """
        email = self.cleaned_data.get("email")

        if Person.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe una persona con este correo electrónico.")

        return email
