from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import RegisterForm, UpdatePointsForm
from .models import Register
from apps.configs.models import Config
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import F, Value, IntegerField
from django.db.models.functions import Coalesce, Cast
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    DetailView
)
from django.core.exceptions import PermissionDenied


def solo_superusuario(user):
    """
    Método para saber si el usuario es superusuario.
    """
    return user.is_superuser


@login_required
def home(request):
    return render(request, 'registers/home.html')


@login_required
def create_update_register(request):
    """
    Vista para crear o actualizar la quiniela del usuario. Si el usuario ya
    tiene una quiniela, cargamos esa quiniela para mostrarla en el formulario.
    """
    # Buscamos la quiniela del usuario, si existe. Si no existe, quiniela será None
    quiniela = Register.objects.filter(usuario_registro=request.user).first()
    config_instance = Config.objects.first()

    # Variable para saber si es una creación (no existía quiniela)
    is_creating = quiniela is None

    # Si el formulario se envió por POST, procesamos los datos
    if request.method == 'POST':
        if config_instance and config_instance.disable_update_quiniela:
            messages.error(request, "Lo sentimos, el periodo de modificación ha finalizado.")
            return redirect('registers:home')
        # Si quiniela es None, el formulario permitirá crear una nueva quiniela,
        # si quiniela no es None, el formulario permitirá actualizar la quiniela
        # existente

        form = RegisterForm(request.POST, instance=quiniela)
        # Si el formulario es válido, guardamos la quiniela y asignando el usuario
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario_registro = request.user
            registro.save()

            # Enviar correo solo si es la primera vez que crea la quiniela
            if is_creating:
                send_quiniela_creation_email(request.user)
                messages.success(request, "¡Quiniela creada exitosamente! Se ha enviado un correo de confirmación.")
            else:
                messages.success(request, "¡Quiniela actualizada exitosamente!")

            return redirect('registers:home')
    # Si no es POST, simplemente mostramos el formulario, cargando la quiniela
    # si existe
    else:
        # Si no es POST, simplemente mostramos el formulario, cargando la
        # quiniela si existe.
        form = RegisterForm(instance=quiniela)

    return render(request, 'registers/create.html', {
        'form': form,
        'quiniela': quiniela,
        # Indicador para la plantilla de si estamos creando o actualizando
        'update': quiniela is not None,
        'config_instance': config_instance
    })


def send_quiniela_creation_email(user):
    """
    Función auxiliar para enviar correo de confirmación de creación de quiniela
    """
    subject = "Quiniela - Mundial 2026 | Quiniela creada"

    message = (
        f"Hola {user.first_name if user.first_name else user.username},\n\n"
        f"¡Felicidades! Tu quiniela para el Mundial 2026 ha sido creada exitosamente.\n\n"
        f"Ya puedes consultar y seguir tu participación en el sistema.\n\n"
        f"Si en algún momento necesitas actualizar tus pronósticos, recuerda que "
        f"tendrás un periodo habilitado para hacerlo.\n\n"
    )

    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )

        # Enviamos correo a NOTIFICATION_EMAIL.
        send_mail(
            subject=f"Nuevo quiniela registrada de: {user.username}",
            message=(
                f"Se ha registrado una nueva quiniela en el sistema:\n\n"
                f"Nombre y Apellido: {user.first_name} {user.last_name}\n"
                f"Usuario: {user.username}\n"
                f"Email: {user.email}\n"
                f"Fecha de registro: {user.date_joined.strftime('%d/%m/%Y')}\n\n"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.NOTIFICATION_EMAIL],
            fail_silently=True,
        )
    except Exception as e:
        # Registrar el error en logs sin detener el flujo
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error al enviar correo a {user.email}: {str(e)}")


@login_required
def detail_register(request, pk):
    register = get_object_or_404(Register, pk=pk)
    context = {'register': register}
    return render(request, 'registers/detail.html', context)


@login_required
@user_passes_test(solo_superusuario, login_url='registers:home')
def list(request):
    """
    Vista para mostrar la lista de quinielas registradas por los usuarios inactivos.
    """
    # Filtramos por usuarios cuyo estado 'is_active' sea True
    registers = Register.objects.filter(
        usuario_registro__is_active=True
    ).order_by('-updated_at')

    context = {'registers': registers}
    return render(request, 'registers/list.html', context)


@login_required
@user_passes_test(solo_superusuario, login_url='registers:home')
def update_points(request, pk):
    """
    Vista para actualizar los puntos de las quinielas.
    Bloquea el acceso si el usuario dueño de la quiniela está inactivo.
    """
    quiniela = get_object_or_404(Register, pk=pk)

    # Si el usuario dueño de la quiniela no está activo, no permitimos actualizar
    # los puntos.
    if not quiniela.usuario_registro.is_active:
        messages.error(request, "La quiniela no está disponible o el usuario está inactivo.")
        return redirect('registers:home')

    # Si el formulario se envió por POST, procesamos los datos para actualizar
    # los puntos.
    if request.method == 'POST':
        form = UpdatePointsForm(request.POST, instance=quiniela)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Puntos actualizados!")
            return redirect('registers:home')
    else:
        form = UpdatePointsForm(instance=quiniela)

    context = {
        'form': form,
        'quiniela': quiniela
    }
    return render(request, 'registers/update_points.html', context)


@login_required
def delete_register(request, pk):
    register = get_object_or_404(Register, pk=pk)
    if request.method == 'POST':
        register.delete()
        return redirect('registers:home')
    
    context = {'register': register}
    return render(request, 'registers/delete.html', context)


@login_required
def ranking(request):
    # Convertir cada campo a IntegerField y manejar valores nulos
    puntos_sum = Cast(Coalesce('puntos_game_1', Value('0')), IntegerField())

    # Sumamos los puntos de cada juego del 1 al 72, manejando valores nulos
    for i in range(2, 73):
        # Convertimos el campo a IntegerField y manejamos valores nulos con Coalesce
        puntos_sum += Cast(Coalesce(f'puntos_game_{i}', Value('0')), IntegerField())

    # Agregamos el filtro para usuarios activos
    registers = Register.objects.filter(
        usuario_registro__is_active=True
    ).annotate(
        total_puntos=puntos_sum
    ).order_by('-total_puntos')

    config_instance = Config.objects.first()

    context = {
        'registers': registers,
        'config_instance': config_instance
    }
    return render(request, 'registers/ranking.html', context)


class RegisterDetailView(LoginRequiredMixin, DetailView):
    model = Register
    template_name = "registers/register_detail.html"
    context_object_name = "quiniela"

    def dispatch(self, request, *args, **kwargs):
        """
        Verifica si la vista de registros está habilitada antes de mostrar el detalle.
        """
        # Obtener la configuración actual (asumiendo que hay un solo registro de Config)
        config = Config.objects.first()

        # Si disable_view_register es True, no permitir el acceso
        if config and config.disable_view_register:
            # Redirigir a otra página (elige la que prefieras)
            return redirect('registers:ranking')  # Redirige al ranking

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Obtiene el objeto y verifica si el usuario del registro está activo.
        """
        # Obtenemos el objeto actual (esto maneja el 404 si el ID no existe)
        self.object = self.get_object()

        # Validamos si el usuario relacionado está inactivo
        if not self.object.usuario_registro.is_active:
            messages.error(request, "El usuario de este registro no está activo.")
            return redirect('registers:ranking')

        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


@login_required
def groups(request):
    return render(request, 'registers/groups.html')


@login_required
def results(request):
    return render(request, 'registers/results.html')


@login_required
@user_passes_test(solo_superusuario, login_url='registers:home')
def ranking_for_admin(request):
    # Convertir cada campo a IntegerField y manejar valores nulos
    puntos_sum = Cast(Coalesce('puntos_game_1', Value('0')), IntegerField())

    # Sumamos los puntos de cada juego del 1 al 72, manejando valores nulos
    for i in range(2, 73):
        # Convertimos el campo a IntegerField y manejamos valores nulos con Coalesce
        puntos_sum += Cast(Coalesce(f'puntos_game_{i}', Value('0')), IntegerField())

    # Agregamos el filtro para usuarios activos
    registers = Register.objects.filter(
        usuario_registro__is_active=True
    ).annotate(
        total_puntos=puntos_sum
    ).order_by('-total_puntos')

    context = {
        'registers': registers,
    }
    return render(request, 'registers/ranking_for_admin.html', context)


class RegisterDetailViewForAdmin(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Register
    template_name = "registers/register_detail_for_admin.html"
    context_object_name = "quiniela"

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

    def get_queryset(self):
        """
        Filtra los registros para devolver solo aquellos cuyo usuario esté activo.
        """
        queryset = super().get_queryset()
        return queryset.filter(usuario_registro__is_active=True)