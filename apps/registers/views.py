from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Register
from .forms import RegisterForm
import openpyxl
from django.http import HttpResponse
from django.db.models import Count
import json
from django.http import JsonResponse


@login_required
def home(request):
    query_cedula = request.GET.get('q', '')
    query_nombres = request.GET.get('n', '')
    query_apellidos = request.GET.get('a', '')
    query_fecha_nacimiento = request.GET.get('f', '')
    query_libro = request.GET.get('l', '')

    # QuerySet para la TABLA (mantiene el orden alfabético por nombres)
    registers = Register.objects.all().order_by('nombres')

    # Filtro por cédula
    if query_cedula:
        registers = registers.filter(cedula__icontains=query_cedula)
    
    # Filtro por nombres
    if query_nombres:
        registers = registers.filter(nombres__icontains=query_nombres)
    
    # Filtro por apellidos
    if query_apellidos:
        registers = registers.filter(apellidos__icontains=query_apellidos)

    # Filtro por fecha de nacimiento
    if query_fecha_nacimiento:
        registers = registers.filter(fecha_nacimiento=query_fecha_nacimiento)

    # Filtro por libro
    if query_libro:
        registers = registers.filter(libro__icontains=query_libro)

    SEXOS = [
        ("M", "M"),
        ("F", "F"),
    ]

    # Construcción del contexto
    context = {
        'registers': registers,
        'sexos': SEXOS,
        'query_cedula': query_cedula,
        'query_nombres': query_nombres,
        'query_apellidos': query_apellidos,
        'query_fecha_nacimiento': query_fecha_nacimiento,
        'query_libro': query_libro,
    }

    return render(request, 'registers/home.html', context)


@login_required
def create_register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Creamos la instancia en memoria sin guardar en la BD aún
            nuevo_registro = form.save(commit=False)

            # Asignamos el usuario autenticado (tu modelo User personalizado)
            nuevo_registro.usuario_registro = request.user

            # Guardamos definitivamente
            nuevo_registro.save()

            return redirect('registers:home')
    else:
        form = RegisterForm()
    
    SEXOS = [
        ("M", "M"),
        ("F", "F"),
    ]

    context = {
        'form': form,
        'sexos': SEXOS,
    }
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

    SEXOS = [
        ("M", "M"),
        ("F", "F"),
    ]

    context = {
        'form': form,
        'register': register,
        'sexos': SEXOS,
    }
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


def api_parroquias(request):
    """API para obtener parroquias por municipio"""
    municipio_id = request.GET.get('municipio_id')
    if municipio_id:
        parroquias = Parroquia.objects.filter(municipio_id=municipio_id).values('id', 'nombre')
        return JsonResponse(list(parroquias), safe=False)
    return JsonResponse([], safe=False)


@login_required
def graphics(request):
    # QuerySet para la TABLA (mantiene el orden cronológico)
    registers = Register.objects.all().order_by('-created_at')

    # Obtener lista de municipios con ID y nombre para el select
    municipios = Municipio.objects.all().order_by('nombre')

    # CORREGIDO: Contar registros por municipio (no por parroquia)
    stats = registers.values('municipio__nombre').annotate(
        total=Count('id')  # o Count('*') o simplemente Count('id')
    ).order_by('municipio__nombre')

    chart_labels = [item['municipio__nombre'] for item in stats if item['municipio__nombre']]  # Filtrar None
    chart_data = [item['total'] for item in stats if item['municipio__nombre']]

    context = {
        'municipios': municipios,
        'registers': registers,          # Datos para la tabla
        'total_registros': registers.count(),  # Total de registros
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }

    return render(request, 'registers/graphics.html', context)
