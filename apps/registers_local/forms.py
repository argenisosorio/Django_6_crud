from django import forms
from .models import Register_local

class Register_localForm(forms.ModelForm):
    class Meta:
        model = Register_local

        #fields = '__all__'

        # Excluimos el campo de usuario para que no aparezca en el HTML
        exclude = ['usuario_registro']
