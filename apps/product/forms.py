from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    """
    A ModelForm for creating and updating Product instances.
    """

    """
    Validación personalizada para el campo 'name' del formulario.
    Esta función se ejecuta automáticamente durante la validación del formulario.
    Verifica que el nombre del producto no contenga la palabra 'test' (en
    cualquier combinación de mayúsculas y minúsculas). Si se encuentra la
    palabra 'test', se lanza una ValidationError con un mensaje específico. Si
    el nombre es válido, se devuelve el valor limpio del campo 'name'.
    """
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if "test" in name.lower():
            raise forms.ValidationError("No puedes usar la palabra 'test' en el nombre del producto.")
        return name

    """
    Validación personalizada para el campo 'price' del formulario. Esta función
    se ejecuta automáticamente durante la validación del formulario. Verifica
    que el precio del producto sea un número positivo. Si el precio es menor o
    igual a cero, se lanza una ValidationError con un mensaje específico. Si el
    precio es válido, se devuelve el valor limpio del campo 'price'.
    """
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("El precio debe ser un número positivo.")
        return price

    class Meta:
        """
        Metadata class defining the form's relationship to the model.
        """
        model = Product

        fields = [
            'name',
            'price',
        ]
