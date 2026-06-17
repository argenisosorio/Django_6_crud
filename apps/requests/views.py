from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Request
from .forms import RequestForm
import openpyxl
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse


@login_required
def home(request):
    requests = Request.objects.all().order_by('-created_at')

    context = {
        'requests': requests,
    }

    return render(request, 'requests/home.html', context)
