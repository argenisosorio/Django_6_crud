from django import forms
from .models import Register_extern

class Register_externForm(forms.ModelForm):
    class Meta:
        model = Register_extern

        #fields = '__all__'

        # Excluimos el campo de usuario para que no aparezca en el HTML
        exclude = ['usuario_registro']
