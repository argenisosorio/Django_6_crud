from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Register
from .forms import RegisterForm
import openpyxl
from django.http import HttpResponse


@login_required
def home(request):
    registers = Register.objects.all().order_by('-created_at')

    if 'export' in request.GET:
        return export_registers_excel(registers)

    context = {
        'registers': registers,
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


def export_registers_excel(queryset):
    """Función auxiliar para generar el archivo .xlsx"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte de Registros"

    # Definir encabezados
    headers = [
        'Nombres y Apellidos', 'Puesto de trabajo', 'N de Bien CPU',
        'Capacidad DD', 'Serial DD', 'Modelo DD', 'Tipo DD', 'Procesador',
        'Cantidad de memorias', 'Capacidad de memorias', 'Modelo de memorias',
        'RAM máxima', 'Cantidad de zócalos de memoria', 'NB Monitor',
        'Modelo Monitor', 'Serial Monitor', 'NB Mouse', 'Serial Mouse',
        'NB Teclado', 'Marca Teclado', 'Modelo Teclado', 'Serial Teclado',
        'UPS', 'Marca UPS', 'Modelo UPS', 'Serial UPS'
    ]
    ws.append(headers)

    # Estilo básico para la cabecera (Opcional pero recomendado)
    for cell in ws[1]:
        cell.font = openpyxl.styles.Font(bold=True)

    # Agregar los datos del QuerySet filtrado
    for reg in queryset:
        ws.append([
            reg.nombres_apellidos,
            reg.puesto_trabajo,
            reg.n_bien_cpu,
            reg.cap_dd,
            reg.serial_dd,
            reg.modelo_dd,
            reg.tipo_dd,
            reg.procesador,
            reg.cant_memorias,
            reg.cap_memorias,
            reg.modelo_memorias,
            reg.max_ram,
            reg.cant_zoc_mem,
            reg.nb_monitor,
            reg.mod_monitor,
            reg.serial_monitor,
            reg.nb_mouse,
            reg.serial_mouse,
            reg.nb_teclado,
            reg.marca_teclado,
            reg.mod_teclado,
            reg.serial_teclado,
            reg.ups,
            reg.marca_ups,
            reg.mod_ups,
            reg.serial_ups
        ])

    # Ajustar ancho de columnas automáticamente
    for col in ws.columns:
        max_length = 0
        column = col[0].column_letter
        for cell in col:
            if cell.value:
                max_length = max(max_length, len(str(cell.value)))
        ws.column_dimensions[column].width = max_length + 2

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_oxigeno.xlsx"'
    wb.save(response)

    return response
