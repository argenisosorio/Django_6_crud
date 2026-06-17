from django import forms
from .models import Request

class RequestForm(forms.ModelForm):
    class Meta:
        model = Request

        #fields = '__all__'

        # Excluimos el campo de usuario para que no aparezca en el HTML
        exclude = ['usuario_registro']
