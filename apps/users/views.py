from django.contrib.auth import get_user_model, login, logout
from django.core.mail import send_mail
from django.conf import settings
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
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


class LoginView(AuthLoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirigir a Home después de iniciar sesión exitosamente."""
        return reverse_lazy("registers:home")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:login")

    def post(self, request):
        logout(request)
        return redirect("users:login")


"""
Vista para el registro de nuevos usuarios. Después de registrarse, el usuario es
autenticado automáticamente y redirigido a Home.
"""
class SignUpView(CreateView):
    model = get_user_model()
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("registers:home")

    def form_valid(self, form):
        # 1. Ejecutamos super().form_valid(form) para guardar el usuario en la DB
        response = super().form_valid(form)

        # 2. El usuario guardado ahora está en self.object
        user = self.object

        # 3. Lógica de envío de correo
        try:
            subject = "Bienvenido al Sistema - Tus credenciales"
            message = (
                f"Hola {user.username},\n\n"
                f"Tu registro ha sido exitoso.\n"
                f"Ya puedes acceder a la plataforma con tu usuario: {user.username}\n"
                f"Si no recuerdas tu contraseña, contacta al administrador."
            )

            # Enviamos el correo al usuario recién registrado
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True, # Evita que la app de error 500 si el servidor de correo falla
            )
        except Exception as e:
            # Aquí podrías usar un logger para registrar el error sin interrumpir al usuario
            print(f"Error enviando correo: {e}")

        # 4. Autenticamos al usuario automáticamente
        login(self.request, user)

        return response


class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "users/user_detail.html"
    context_object_name = "user"


class UserCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:user_list")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users:user_list")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:user_list")


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Vista para que los usuarios puedan actualizar su propio perfil.
    """
    model = get_user_model()
    template_name = "users/profile_form.html"
    form_class = ProfileForm
    success_url = reverse_lazy("registers:home")
