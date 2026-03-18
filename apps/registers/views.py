from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Register
from .forms import RegisterForm

@login_required
def home(request):
    query_cedula = request.GET.get('q', '')
    query_parroquia = request.GET.get('p', '')

    registers = Register.objects.all().order_by('-created_at')

    if query_cedula:
        registers = registers.filter(cedula__icontains=query_cedula)
    
    if query_parroquia:
        # Aquí usamos coincidencia exacta porque viene de un select
        registers = registers.filter(parroquia=query_parroquia)

    # Definimos la lista aquí o impórtala de tu modelo
    parroquias_list = [
        "Antonio Spinetti Dini", "Arias", "Caracciolo Parra Pérez",
        "Domingo Peña", "El Llano", "El Sagrario", "Gonzalo Picón Febres",
        "Jacinto Plaza", "Lasso de la Vega", "Juan Rodríguez Suárez",
        "Mariano Picón Salas", "Milla", "Osuna Rodríguez"
    ]

    context = {
        'registers': registers,
        'query_cedula': query_cedula,
        'query_parroquia': query_parroquia,
        'parroquias_list': parroquias_list,
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