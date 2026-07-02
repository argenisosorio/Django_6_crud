import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = [
            'name',
            'email',
            'age'
        ]

    # Validación para el nombre
    def clean_name(self):
        name = self.cleaned_data.get('name')

        # Si el usuario no envió nada lanza el error de requerido
        if not name:
            raise ValidationError('El nombre es requerido.')

        # Validar que el nombre solo contenga letras y espacios
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', name):
            raise ValidationError(
                'El nombre solo debe contener letras y espacios, sin números ni caracteres especiales.'
            )

        return name

    # Validación para el email
    def clean_email(self):
        email = self.cleaned_data.get('email')

        # Si el usuario no envió nada lanza el error de requerido
        if not email:
            raise ValidationError('El correo electrónico es requerido.')

        # Validar que el email tenga un formato válido
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError(
                'El correo electrónico no tiene un formato válido.'
            )

        return email

    # Validación para la edad
    def clean_age(self):
        age = self.cleaned_data.get('age')

        # Si el usuario no envió nada lanza el error de requerido
        if not age:
            raise ValidationError('La edad es requerida.')

        # Validar que la edad sea un número entero
        try:
            age_int = int(age)
        except (ValueError, TypeError):
            raise ValidationError('La edad debe ser un número entero.')

        # Validar que sea un entero positivo
        if age_int <= 0:
            raise ValidationError('La edad debe ser mayor de 0 años.')

        # Validar que sea mayor de 18
        if age_int < 18:
            raise ValidationError('La edad debe ser mayor de 18 años.')

        return age
