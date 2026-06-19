from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse
from .forms import RegisterFuelForm
from .models import RegisterFuel, FuelStorage


@login_required
def home(request):
    registers = RegisterFuel.objects.all().order_by('-created_at')

    # Construcción del contexto
    context = {
        'registers': registers,
    }

    return render(request, 'registers/home.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = RegisterFuelForm(request.POST)
        if form.is_valid():
            # Creamos la instancia en memoria sin guardar en la BD aún
            nuevo_registro = form.save(commit=False)

            # Asignamos el usuario autenticado (tu modelo User personalizado)
            nuevo_registro.register_by = request.user

            # Guardamos definitivamente
            nuevo_registro.save()

            return redirect('registers:home')
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
