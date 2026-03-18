from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Register
from .forms import RegisterForm

@login_required
def home(request):
    # Capturamos ambos parámetros de búsqueda
    query_cedula = request.GET.get('q', '')
    query_parroquia = request.GET.get('p', '')

    # Empezamos con todos los registros
    registers = Register.objects.all().order_by('-created_at')

    # Filtro por Cédula (si existe)
    if query_cedula:
        registers = registers.filter(cedula__icontains=query_cedula)

    # Filtro por Parroquia (si existe)
    if query_parroquia:
        registers = registers.filter(parroquia__icontains=query_parroquia)

    context = {
        'registers': registers,
        'query_cedula': query_cedula,
        'query_parroquia': query_parroquia,
    }
    return render(request, 'registers/home.html', context)

@login_required
def create_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('registers:home')
    else:
        form = RegisterForm()
    
    context = {'form': form}
    return render(request, 'registers/create.html', context)

@login_required
def detail_register(request, pk):
    register = get_object_or_404(Register, pk=pk)
    context = {'register': register}
    return render(request, 'registers/detail.html', context)

@login_required
def update_register(request, pk):
    register = get_object_or_404(Register, pk=pk)
    if request.method == 'POST':
        form = RegisterForm(request.POST, instance=register)
        if form.is_valid():
            form.save()
            return redirect('registers:detail', pk=register.pk)
    else:
        form = RegisterForm(instance=register)
    
    context = {'form': form, 'register': register}
    return render(request, 'registers/update.html', context)

@login_required
def delete_register(request, pk):
    register = get_object_or_404(Register, pk=pk)
    if request.method == 'POST':
        register.delete()
        return redirect('registers:home')
    
    context = {'register': register}
    return render(request, 'registers/delete.html', context)