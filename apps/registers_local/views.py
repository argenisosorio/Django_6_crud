from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Register_local
from .forms import Register_localForm
import openpyxl
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse


@login_required
def home(request):
    registers = Register_local.objects.all().order_by('-created_at')

    # Construcción del contexto
    context = {
        'registers': registers,
    }

    return render(request, 'registers_local/home.html', context)


@login_required
def create_register(request):
    if request.method == 'POST':
        form = Register_localForm(request.POST)
        if form.is_valid():
            # Creamos la instancia en memoria sin guardar en la BD aún
            nuevo_registro = form.save(commit=False)

            # Asignamos el usuario autenticado (tu modelo User personalizado)
            nuevo_registro.usuario_registro = request.user

            # Guardamos definitivamente
            nuevo_registro.save()

            return redirect('registers_local:home')
    else:
        form = Register_localForm()
    
    context = {
        'form': form,
    }

    return render(request, 'registers_local/create.html', context)

@login_required
def detail_register(request, pk):
    register = get_object_or_404(Register_local, pk=pk)
    context = {'register': register}
    return render(request, 'registers_local/detail.html', context)


@login_required
def update_register(request, pk):
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
def delete_register(request, pk):
    register = get_object_or_404(Register_local, pk=pk)
    if request.method == 'POST':
        register.delete()
        return redirect('registers_local:home')
    
    context = {'register': register}
    return render(request, 'registers_local/delete.html', context)


def export_registers_excel(queryset):
    """Función auxiliar para generar el archivo .xlsx"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte de Registros"

    # Definir encabezados
    headers = [
        'Nombres', 'Apellidos', 'Cédula', 'Teléfono', 'Dirección', 'Municipio',
        'Parroquia', 'Fecha de Registro', 'Fecha de Despacho', 'Cantidad',
        'Tamaño', 'Visitado', 'Documentos completos'
    ]
    ws.append(headers)

    # Estilo básico para la cabecera (Opcional pero recomendado)
    for cell in ws[1]:
        cell.font = openpyxl.styles.Font(bold=True)

    # Agregar los datos del QuerySet filtrado
    for reg in queryset:
        ws.append([
            reg.nombres,
            reg.apellidos,
            reg.cedula,
            reg.telefono,
            reg.direccion,
            reg.municipio.nombre if reg.municipio else '',
            reg.parroquia.nombre if reg.parroquia else '',
            reg.fecha_registro.strftime('%d/%m/%Y') if reg.fecha_registro else '',
            reg.fecha_despacho.strftime('%d/%m/%Y') if reg.fecha_despacho else 'Pendiente',
            reg.cantidad,
            reg.tamano_cilindro,
            "Sí" if reg.visitado else "No",
            "Sí" if reg.documentos_completos else "No"
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
