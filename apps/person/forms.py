from django import forms
from .models import Person

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'age']

        # Personalización de mensajes de error
        error_messages = {
            'name': {
                'required': "El campo Nombre es obligatorio.",
            },
            'email': {
                'required': "El campo Correo electrónico es obligatorio.",
                'invalid': "El campo Correo electrónico debe ser un correo válido.",
            },
            'age': {
                'required': "El campo Edad es obligatorio.",
                'invalid': "El campo Edad debe ser un número entero.",
            },
        }

        # Agregamos clases de Bootstrap para que se vea bien en tu red local
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': ''}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'max': '120'}),
        }
