from django.contrib.auth import get_user_model, login, logout
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.http import HttpResponseRedirect
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


class LoginView(AuthLoginView):
    """
    Vista para iniciar sesión de usuarios.
    """
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirigir a la lista de usuarios después del login"""
        return reverse_lazy("registers_local:home")


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


class SignUpView(CreateView):
    """
    Vista para registrar nuevos usuarios.
    """
    model = get_user_model()
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


# ==================== VISTAS CRUD DE USUARIOS ====================

class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = "users/list.html"
    context_object_name = "users"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "users/detail.html"
    context_object_name = "user"


class UserCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    template_name = "users/form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")

    # Sobrescribimos el método form_valid para guardar el usuario activo.
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        self.object = user
        return redirect(self.success_url)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "users/update.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users:list")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = "users/confirm_delete.html"
    success_url = reverse_lazy("users:list")
