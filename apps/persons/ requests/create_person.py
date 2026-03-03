from django import forms
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator

from apps.persons.models.employee import Employee


class CreatePersonRequest(forms.Form):
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(validators=[MinLengthValidator(8)])
    id_number = forms.CharField(max_length=20)
    position = forms.CharField(max_length=100)
    department = forms.CharField(max_length=100)

    def clean_username(self):
        User = get_user_model()
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_id_number(self):
        id_number = self.cleaned_data.get("id_number")
        if Employee.objects.filter(id_number=id_number).exists():
            raise forms.ValidationError("ID number already exists.")
        return id_number
