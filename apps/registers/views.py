from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UpdatePointsForm
from .models import Register
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse
from django.contrib import messages


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

    # Si el formulario se envió por POST, procesamos los datos
    if request.method == 'POST':
        # Si quiniela es None, el formulario permitirá crear una nueva quiniela,
        # si quiniela no es None, el formulario permitirá actualizar la quiniela
        # existente
        form = RegisterForm(request.POST, instance=quiniela)
        # Si el formulario es válido, guardamos la quiniela y asignando el usuario
        if form.is_valid():
            registro = form.save(commit=False)
            registro.usuario_registro = request.user
            registro.save()
            messages.success(request, "¡Quiniela guardada!")
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
        'update': quiniela is not None
    })

@login_required
def detail_register(request, pk):
    register = get_object_or_404(Register, pk=pk)
    context = {'register': register}
    return render(request, 'registers/detail.html', context)


@login_required
def list(request):
    """
    Vista para mostrar la lista de quinielas registradas por los usuarios.
    """
    registers = Register.objects.all()
    context = {'registers': registers}
    return render(request, 'registers/list.html', context)


@login_required
def update_points(request, pk):
    """
    Vista para actualizar los puntos de las quinielas
    """
    quiniela = get_object_or_404(Register, pk=pk)

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
def config(request):
    """
    Vista para mostrar la página de configuraciones general de la aplicación.
    """
    return render(request, 'registers/config.html')


@login_required
def ranking(request):
    return render(request, 'registers/ranking.html')
