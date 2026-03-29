from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "nickname",
            "favorite_country"
        )


class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "nickname",
            "favorite_country"
        )
