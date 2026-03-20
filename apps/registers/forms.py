from django import forms
from .models import Register

class RegisterForm(forms.ModelForm):
    """
    A ModelForm for creating and updating Register instances.
    """

    class Meta:
        model = Register

        #fields = '__all__'

        # Excluimos el campo de usuario para que no aparezca en el HTML
        exclude = ['usuario_registro']
