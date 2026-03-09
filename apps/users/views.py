from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm


"""
Vistas basadas en clases para operaciones CRUD de usuarios y autenticación.

Este módulo expone vistas genéricas basadas en clases que operan en el modelo
de usuario personalizado del proyecto, así como vistas para login y logout.
"""


# ==================== VISTAS DE AUTENTICACIÓN ====================

class LoginView(AuthLoginView):
    """
    Vista para iniciar sesión de usuarios.
    """
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirigir a la lista de usuarios después del login"""
        return reverse_lazy("users:user_list")


class LogoutView(View):
    """
    Vista para cerrar sesión de usuarios.
    """
    def get(self, request):
        logout(request)
        return redirect("users:login")

    def post(self, request):
        logout(request)
        return redirect("users:login")


# ==================== VISTAS CRUD DE USUARIOS ====================

@method_decorator(login_required, name='dispatch')
class UserListView(ListView):
    model = get_user_model()
    template_name = "users/user_list.html"
    context_object_name = "users"


@method_decorator(login_required, name='dispatch')
class UserDetailView(DetailView):
    model = get_user_model()
    template_name = "users/user_detail.html"
    context_object_name = "user"


@method_decorator(login_required, name='dispatch')
class UserCreateView(CreateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:user_list")


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users:user_list")


@method_decorator(login_required, name='dispatch')
class UserDeleteView(DeleteView):
    model = get_user_model()
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:user_list")
