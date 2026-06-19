from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse


@login_required
def home(request):
    data = "Hola"

    # Construcción del contexto
    context = {
        'data': data,
    }

    return render(request, 'registers/home.html', context)
