from django.contrib.auth import get_user_model, login, logout
from django.core.mail import send_mail
from django.conf import settings
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.urls import reverse
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

    def form_valid(self, form):
        # Ejecutamos el login normal
        response = super().form_valid(form)

        # Mensaje de éxito.
        messages.success(self.request, f"¡Bienvenido, {self.request.user.username}!")

        return response

    def get_success_url(self):
        #Redirigir a Home después de iniciar sesión exitosamente.
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
        # 1. Extraemos la contraseña limpia del formulario ANTES de guardar
        # El formulario ya la validó, así que está disponible en cleaned_data
        raw_password = form.cleaned_data.get('password1')

        # 2. Guardamos el usuario (aquí Django ya la cifra en la DB)
        # Ejecutamos super().form_valid(form) para guardar el usuario en la DB
        response = super().form_valid(form)
        user = self.object

        # 3. Lógica de envío de correo con la contraseña en texto plano
        try:
            subject = " Quiniela - Mundial 2026 | Credenciales de acceso"
            message = (
                f"Hola {user.first_name if user.first_name else user.username},\n\n"
                f"Tu registro en el sistema ha sido exitoso.\n\n"
                f"Tus credenciales de acceso son:\n\n"
                f"----------------------------------\n"
                f"Usuario: {user.username}\n"
                f"Contraseña: {raw_password}\n"
                f"----------------------------------\n\n"
            )

            # Enviamos el correo al usuario recién registrado
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True, # Evita que la app de error 500 si el servidor de correo falla.
            )
        except Exception as e:
            # Mensaje de error en consola si el envío de correo falla, pero no
            # interrumpe el flujo de registro.
            print(f"Error al enviar correo: {e}")

        # 4. Autenticamos al usuario automáticamente después de registrarse.
        login(self.request, user)

        messages.success(self.request, f"¡Registro exitoso, {user.username}!")

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


from django.urls import reverse

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "users/profile_form.html"
    form_class = ProfileForm

    def get_object(self, queryset=None):
        """
        Sobrescribimos este método para asegurarnos de que el objeto que se edita
        sea el usuario actualmente autenticado, independientemente del PK en la URL.
        Esto evita que un usuario pueda editar el perfil de otro cambiando el PK
        en la URL.
        """
        return self.request.user

    def get_success_url(self):
        # Le pasamos el PK del usuario actual para que coincida con la URL
        return reverse("users:profile_update", kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        """
        Agregamos un mensaje de éxito después de actualizar el perfil.
        """
        messages.success(self.request, "Perfil actualizado")
        return super().form_valid(form)
