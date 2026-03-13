from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """
    A ModelForm for creating and updating Product instances.
    """

    class Meta:
        """
        Metadata class defining the form's relationship to the model.
        """
        model = Product

        fields = [
            'name',
            'price',
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nombre del producto',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Precio del producto',
                'min': '0',
            }),
        }

        error_messages = {
            'name': {
                'required': 'Este campo es requerido.',
                'max_length': 'Máximo 100 caracteres.',
            },
            'price': {
                'required': 'Este campo es requerido.',
                'min_value': 'No se permiten números negativos.',
            },
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        if name and price:
            if "test" in name.lower() and price > 100:
                raise forms.ValidationError("No puedes usar la palabra 'test' en el nombre si el precio es mayor a 100.")
        return cleaned_data
