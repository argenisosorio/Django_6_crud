from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


"""
Vistas basadas en clases para operaciones CRUD de usuarios.

Este módulo expone un pequeño conjunto de vistas genéricas basadas en clases que
operan en el modelo de usuario personalizado del proyecto. Cada vista establece
un template_name y cuando corresponde, una clase de formulario y una
success_url para las redirecciones tras operaciones exitosas.
"""


class UserListView(ListView):
    model = get_user_model()
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserDetailView(DetailView):
    model = get_user_model()
    template_name = "users/user_detail.html"
    context_object_name = "user"


class UserCreateView(CreateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:user_list")


class UserUpdateView(UpdateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users:user_list")


class UserDeleteView(DeleteView):
    model = get_user_model()
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:user_list")

