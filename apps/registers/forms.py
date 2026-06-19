from django import forms
from .models import RegisterFuel, FuelStorage, FuelStorageLocal, FuelStorageExtern


class FuelStorageForm(forms.ModelForm):
    class Meta:
        model = FuelStorage

        fields = '__all__'


class RegisterFuelForm(forms.ModelForm):
    class Meta:
        model = RegisterFuel

        # Excluimos el campo de usuario para que no aparezca en el HTML
        exclude = ['register_by']


class FuelStorageLocalForm(forms.ModelForm):
    class Meta:
        model = FuelStorageLocal

        fields = '__all__'


class FuelStorageExternForm(forms.ModelForm):
    class Meta:
        model = FuelStorageExtern

        fields = '__all__'
