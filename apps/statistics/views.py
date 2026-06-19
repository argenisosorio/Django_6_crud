from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse
from apps.registers.models import FuelStorage, FuelStorageLocal, FuelStorageExtern


@login_required
def home(request):
    """
    Vista principal para la página de inicio.
    """
    # Recuperamos el objeto FuelStorage original para obtener la capacidad máxima
    fuel_storage_config = FuelStorage.objects.first()
    
    data_FuelStorageLocal = FuelStorageLocal.objects.first()
    data_FuelStorageExtern = FuelStorageExtern.objects.first()
    
    # Guardamos la suma en una variable independiente (un entero)
    total_current_amount = data_FuelStorageLocal.current_amount + data_FuelStorageExtern.current_amount

    # Inicializamos el porcentaje en 0 por seguridad
    percentage = 0

    # Validamos usando el objeto de configuración y su capacidad máxima
    if fuel_storage_config and fuel_storage_config.maximum_capacity > 0:
        percentage = (total_current_amount / fuel_storage_config.maximum_capacity) * 100
        percentage = round(percentage)  # Redondear a entero.

    context = {
        'data_FuelStorage': fuel_storage_config, # Pasamos el objeto original o el total según lo necesites en el HTML
        'total_current_amount': total_current_amount, # Nueva variable con la suma total
        'data_FuelStorageLocal': data_FuelStorageLocal,
        'data_FuelStorageExtern': data_FuelStorageExtern,
        'percentage': percentage,
    }

    return render(request, 'statistics/home.html', context)
