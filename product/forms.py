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
