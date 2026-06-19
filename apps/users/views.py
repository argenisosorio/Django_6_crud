from django.contrib.auth import get_user_model, login, logout
from apps.users.models import User
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm, UpdateUserPasswordForm, ActiveForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as AuthLoginView, PasswordChangeView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View
)

# ==================== VISTAS DE AUTHENTICACIÓN ====================

class LoginView(AuthLoginView):
    """
    Vista para iniciar sesión de usuarios.
    """
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("statistics:home")


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


# ==================== MIXIN DE PROTECCIÓN (SUPERUSER) ====================

class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Mixin personalizado para asegurar que solo los superusuarios 
    puedan acceder a las vistas CRUD.
    """
    # Si la prueba falla, Django lanzará un error 403 (Forbidden) en vez de
    # redirigir al login.
    raise_exception = True 

    def test_func(self):
        # El usuario debe estar autenticado Y ser superusuario
        return self.request.user.is_authenticated and self.request.user.is_superuser


# ==================== VISTAS CRUD DE USUARIOS (PROTEGIDAS) ====================

class UserListView(LoginRequiredMixin, SuperuserRequiredMixin, ListView):
    """
    Vista para listar usuarios.
    """
    model = get_user_model()
    template_name = "users/list.html"
    context_object_name = "users"


class UserCreateView(LoginRequiredMixin, SuperuserRequiredMixin, CreateView):
    """
    Vista para registrar nuevos usuarios.
    """
    model = get_user_model()
    template_name = "users/form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()
        self.object = user
        return redirect(self.success_url)


class UserUpdateView(LoginRequiredMixin, SuperuserRequiredMixin, UpdateView):
    """
    Vista para actualizar usuarios.
    """
    model = get_user_model()
    template_name = "users/update.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users:list")


class UserDeleteView(LoginRequiredMixin, SuperuserRequiredMixin, DeleteView):
    """
    Vista para eliminar usuarios.
    """
    model = get_user_model()
    template_name = "users/confirm_delete.html"
    success_url = reverse_lazy("users:list")


def update_user_password(request, pk):
    """
    Vista basada en función para actualizar la contraseña de un usuario
    específico. Solo accesible para superusuarios.
    """
    user = get_object_or_404(User, pk=pk)

    if not request.user.is_superuser:
        return redirect('users:list')

    if request.method == 'POST':
        # Se pasa 'user' como primer argumento, luego 'request.POST'
        form = UpdateUserPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:list')
        else:
            print(form.errors)
    else:
        # Se pasa 'user' como primer argumento posicional
        form = UpdateUserPasswordForm(user)

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'users/update_user_password.html', context)


class ActivateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    template_name = "users/active_form.html"
    form_class = ActiveForm
    success_url = reverse_lazy("users:list")

    def test_func(self):
        """
        Esta función debe devolver True para permitir el acceso.
        Verifica si el usuario actual es un superusuario.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Define qué pasa si el usuario NO es superusuario.
        """
        return redirect('users:list')
