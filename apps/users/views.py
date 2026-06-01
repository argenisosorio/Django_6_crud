from django.contrib.auth import get_user_model, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm, ProfileForm, UpdateUserActiveForm, UpdatePasswordForm
from apps.users.models  import User
from apps.configs.models import Config
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView as AuthLoginView
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

    def get_context_data(self, **kwargs):
        # 1. Llamamos al contexto base de la CreateView (que trae el formulario)
        context = super().get_context_data(**kwargs)

        # 2. Agregamos nuestra instancia de configuración
        context['config_instance'] = Config.objects.first()

        return context

    def form_invalid(self, form):
        username = form.cleaned_data.get('username') or self.request.POST.get('username')

        if username:
            User = get_user_model()
            try:
                # Buscar al usuario en la base de datos.
                user = User.objects.get(username=username)

                # Verificamos si está activo o no.
                if user.is_active:
                    pass
                else:
                    messages.error(self.request, "Tu cuenta se encuentra (Inactiva). Contacta al Administrador.")
                    return redirect('users:login')

            except User.DoesNotExist:
                pass
        else:
            pass

        # Llamamos al comportamiento por defecto
        return super().form_invalid(form)

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

    def dispatch(self, request, *args, **kwargs):
        config_instance = Config.objects.first()
        # Verificamos si el registro está deshabilitado
        if config_instance.disable_registration:
            messages.error(request, "Lo sentimos, el periodo de registro ha finalizado")
            return redirect('registers:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # 1. Llamamos al contexto base de la CreateView (que trae el formulario)
        context = super().get_context_data(**kwargs)

        # 2. Agregamos nuestra instancia de configuración
        context['config_instance'] = Config.objects.first()

        return context

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

            # Lógica para los correos de notificación al Admin.
            # Validamos si es una lista/tupla, si es un string simple lo convertimos a lista.
            admins_list = settings.NOTIFICATION_EMAIL
            if isinstance(admins_list, str):
                admins_list = [admins_list]

            # Enviamos la notificación (Django enviará un correo a cada integrante de la lista)
            if admins_list:
                send_mail(
                    subject=f"Nuevo registro: {user.username}",
                    message=(
                        f"Se ha registrado un nuevo usuario en el sistema:\n\n"
                        f"Nombre y Apellido: {user.first_name} {user.last_name}\n"
                        f"Usuario: {user.username}\n"
                        f"Email: {user.email}\n"
                        f"Fecha de registro: {user.date_joined.strftime('%d/%m/%Y')}\n\n"
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=admins_list, # <--- Pasamos la lista procesada aquí
                    fail_silently=True,
                )

        except Exception as e:
            # Mensaje de error en consola si el envío de correo falla, pero no
            # interrumpe el flujo de registro.
            print(f"Error al enviar correo: {e}")

        # 4. Autenticamos al usuario automáticamente después de registrarse.
        login(self.request, user)

        messages.success(self.request, f"¡Registro exitoso, {user.username}!")

        return response


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = get_user_model()
    template_name = "users/user_list.html"
    context_object_name = "users"

    def test_func(self):
        """
        Esta función debe devolver True para permitir el acceso.
        Verifica si el usuario actual es un superusuario.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Opcional: Define qué pasa si el usuario NO es superusuario.
        Por defecto redirige al login, pero aquí puedes mandarlo al home 
        con un mensaje de error.
        """
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(self.request, "No tienes permisos para acceder a esta sección.")
        return redirect('registers:home')


class UserDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = get_user_model()
    template_name = "users/user_detail.html"
    context_object_name = "user"

    def test_func(self):
        """
        Esta función debe devolver True para permitir el acceso.
        Verifica si el usuario actual es un superusuario.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Opcional: Define qué pasa si el usuario NO es superusuario.
        Por defecto redirige al login, pero aquí puedes mandarlo al home 
        con un mensaje de error.
        """
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(self.request, "No tienes permisos para acceder a esta sección.")
        return redirect('registers:home')


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:user_list")

    def test_func(self):
        """
        Esta función debe devolver True para permitir el acceso.
        Verifica si el usuario actual es un superusuario.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Opcional: Define qué pasa si el usuario NO es superusuario.
        Por defecto redirige al login, pero aquí puedes mandarlo al home 
        con un mensaje de error.
        """
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(self.request, "No tienes permisos para acceder a esta sección.")
        return redirect('registers:home')


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users:user_list")

    def test_func(self):
        """
        Esta función debe devolver True para permitir el acceso.
        Verifica si el usuario actual es un superusuario.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Opcional: Define qué pasa si el usuario NO es superusuario.
        Por defecto redirige al login, pero aquí puedes mandarlo al home 
        con un mensaje de error.
        """
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(self.request, "No tienes permisos para acceder a esta sección.")
        return redirect('registers:home')


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = get_user_model()
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:user_list")

    def test_func(self):
        """
        Esta función debe devolver True para permitir el acceso.
        Verifica si el usuario actual es un superusuario.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Opcional: Define qué pasa si el usuario NO es superusuario.
        Por defecto redirige al login, pero aquí puedes mandarlo al home 
        con un mensaje de error.
        """
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(self.request, "No tienes permisos para acceder a esta sección.")
        return redirect('registers:home')


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


class UpdateActiveUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = get_user_model()
    template_name = "users/update_active_user_form.html"
    form_class = UpdateUserActiveForm
    success_url = reverse_lazy("users:user_list")

    def test_func(self):
        """
        Esta función debe devolver True para permitir el acceso.
        Verifica si el usuario actual es un superusuario.
        """
        return self.request.user.is_superuser

    def handle_no_permission(self):
        """
        Opcional: Define qué pasa si el usuario NO es superusuario.
        Por defecto redirige al login, pero aquí puedes mandarlo al home 
        con un mensaje de error.
        """
        from django.contrib import messages
        from django.shortcuts import redirect

        messages.error(self.request, "No tienes permisos para acceder a esta sección.")
        return redirect('registers:home')


def update_user_password(request, pk):
    """
    Vista basada en función para actualizar la contraseña de un usuario
    específico. Solo accesible para superusuarios.
    """
    user = get_object_or_404(User, pk=pk)

    print(f"---- Usuario a actualizar contraseña: {user.username} (ID: {user.pk})")

    # Verificamos permisos de superusuario
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect('registers:home')

    if request.method == 'POST':
        print("---- Entro por POST")
        form = UpdatePasswordForm(request.POST, instance=user)
        if form.is_valid():
            # Guardamos la nueva contraseña (Django se encarga de cifrarla)
            form.save()
            messages.success(request, f"Contraseña de {user.username} actualizada exitosamente.")
            return redirect('users:user_list')
        else:
            print("---- Formulario no válido")
            print(form.errors)
    else:
        print("---- Entro por GET")
        form = UpdatePasswordForm(instance=user)

    context = {
        'form': form,
        'user': user
    }
    return render(request, 'users/update_password_user_form.html', context)
