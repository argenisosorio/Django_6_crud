from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
from datetime import datetime
import json
from django.http import JsonResponse
from .forms import RegisterFuelForm, FuelStorageLocalForm, FuelStorageExternForm
from .models import RegisterFuel, FuelStorage, FuelStorageLocal, FuelStorageExtern
from django.db import transaction


@login_required
def home(request):
    # Obtener y limpiar los parámetros de filtro.
    query_owner_entity = request.GET.get('query_owner_entity', '').strip()
    date_from = request.GET.get('date_from', '').strip()
    date_to = request.GET.get('date_to', '').strip()

    # Traer las opciones directamente desde el Modelo.
    ENTITIES_OWNERS = RegisterFuel.ENTITIES_OWNERS

    # Crear un conjunto (set) de los valores válidos.
    valid_entities = {value for value, _ in ENTITIES_OWNERS}

    # Consultar registros.
    registers = RegisterFuel.objects.all()

    # Filtro seguro de ente propietario.
    if query_owner_entity in valid_entities:
        registers = registers.filter(owner_entity=query_owner_entity)

    # Filtro seguro para Fecha Desde (>=)
    if date_from:
        try:
            # Validamos que la cadena sea una fecha válida (YYYY-MM-DD) antes de filtrar
            datetime.strptime(date_from, '%Y-%m-%d')
            registers = registers.filter(created_at__date__gte=date_from)
        except ValueError:
            date_from = ''  # Si es inválida, la limpiamos para el contexto

    # Filtro seguro para Fecha Hasta (<=)
    if date_to:
        try:
            # Validamos que la cadena sea una fecha válida (YYYY-MM-DD) antes de filtrar
            datetime.strptime(date_to, '%Y-%m-%d')
            registers = registers.filter(created_at__date__lte=date_to)
        except ValueError:
            date_to = ''  # Si es inválida, la limpiamos para el contexto

    # Ordenar los registros por fecha de creación de forma descendente.
    registers = registers.order_by('-created_at')

    # Construcción del contexto.
    context = {
        'registers': registers,
        'ENTITIES_OWNERS': ENTITIES_OWNERS,
        'query_owner_entity': query_owner_entity,
        'date_from': date_from,
        'date_to': date_to,
    }

    return render(request, 'registers/home.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = RegisterFuelForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Crear la instancia en memoria
                new_record = form.save(commit=False)
                new_record.register_by = request.user

                # Determinar cuál almacenamiento usar según el owner_entity
                if new_record.owner_entity == 'CENDITEL':
                    storage = FuelStorageLocal.objects.select_for_update().first()
                    storage_name = "Local (CENDITEL)"
                else:
                    storage = FuelStorageExtern.objects.select_for_update().first()
                    storage_name = "Externo"

                # Validar que el registro de almacenamiento exista
                if storage:
                    # 3. Operar según el tipo de movimiento
                    if new_record.movement_type == 'Entrada':
                        storage.current_amount += new_record.quantity
                    elif new_record.movement_type == 'Salida':
                        # Opcional: Validar que no quede en negativo si lo deseas
                        storage.current_amount -= new_record.quantity

                    # Guardar los cambios en el almacenamiento correspondiente y el registro
                    storage.save()
                    new_record.save()

                    return redirect('registers:home')
                else:
                    # Manejo de error si no existe el registro en la base de datos
                    form.add_error(
                        None, 
                        f"No se encontró el registro de almacenamiento {storage_name}."
                    )
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
