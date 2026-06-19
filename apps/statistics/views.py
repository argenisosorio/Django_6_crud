from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse
from apps.registers.models import FuelStorage


@login_required
def home(request):
    """
    Vista principal para la página de inicio.
    """
    data = FuelStorage.objects.first()

    # Inicializamos el porcentaje en 0 por seguridad
    percentage = 0

    if data and data.maximum_capacity > 0:
        percentage = (data.current_amount / data.maximum_capacity) * 100
        percentage = round(percentage)  # Redonder a entero.

    context = {
        'data': data,
        'percentage': percentage,
    }

    return render(request, 'statistics/home.html', context)
