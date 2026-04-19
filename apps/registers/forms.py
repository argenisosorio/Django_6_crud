from django import forms
from .models import Register

class RegisterForm(forms.ModelForm):
    """
    A ModelForm for creating and updating Register instances.
    """

    class Meta:
        model = Register
        fields = '__all__'
