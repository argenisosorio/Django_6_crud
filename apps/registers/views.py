from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse
from .forms import RegisterFuelForm
from .models import RegisterFuel, FuelStorage
from django.db import transaction


@login_required
def home(request):
    query_owner_entity = request.GET.get('query_owner_entity', '')

    registers = RegisterFuel.objects.all().order_by('-created_at')

    # Filtro por Ente Propietario,
    if query_owner_entity and query_owner_entity in ['CENDITEL', 'ALCARAVAN']:
        registers = registers.filter(owner_entity=query_owner_entity)

    ENTITIES_OWNERS = [
        ("CENDITEL", "CENDITEL"),
        ("ALCARAVAN", "ALCARAVAN"),
    ]

    # Construcción del contexto
    context = {
        'registers': registers,
        'ENTITIES_OWNERS': ENTITIES_OWNERS,
        'query_owner_entity': query_owner_entity
    }

    return render(request, 'registers/home.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = RegisterFuelForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Crear una instancia en memoria sin guardar en la BD aún.
                new_record = form.save(commit=False)
                new_record.register_by = request.user

                # Obtener el registro único de FuelStorage.
                storage = FuelStorage.objects.select_for_update().first()

                if storage:
                    # Validar  el tipo de movimiento y operamos.
                    if new_record.movement_type == 'Entrada':
                        storage.current_amount += new_record.quantity
                    elif new_record.movement_type == 'Salida':
                        storage.current_amount -= new_record.quantity

                    # Guardar cambios en la base de datos.
                    storage.save()
                    new_record.save()

                    return redirect('registers:home')
                else:
                    # Manejo de error si no existe el registro único en FuelStorage
                    form.add_error(None, "No se encontró el registro de almacenamiento de combustible (FuelStorage).")
    else:
        form = RegisterFuelForm()

    context = {
        'form': form,
    }

    return render(request, 'registers/create.html', context)

@login_required
def detail(request, pk):
    register = get_object_or_404(Register_local, pk=pk)
    context = {'register': register}
    return render(request, 'registers_local/detail.html', context)


@login_required
def update(request, pk):
    register = get_object_or_404(Register_local, pk=pk)

    if request.method == 'POST':
        form = Register_localForm(request.POST, instance=register)
        if form.is_valid():
            form.save()
            return redirect('registers_local:detail', pk=register.pk)
    else:
        form = Register_localForm(instance=register)

    context = {
        'form': form,
        'register': register,
    }

    return render(request, 'registers_local/update.html', context)


@login_required
def delete(request, pk):
    register = get_object_or_404(Register_local, pk=pk)
    if request.method == 'POST':
        register.delete()
        return redirect('registers_local:home')

    context = {'register': register}
    return render(request, 'registers_local/delete.html', context)
