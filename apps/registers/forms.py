from django import forms
from .models import Register

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register

        fields = '__all__'
        # Excluimos el campo usuario_registro para que no se muestre en el formulario
        exclude = ['usuario_registro']
