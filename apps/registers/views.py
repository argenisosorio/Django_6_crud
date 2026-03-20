from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Register
from .forms import RegisterForm
import openpyxl
from django.http import HttpResponse
from django.db.models import Count # Importante añadir esto
import json # Para pasar los datos al JS del template


@login_required
def home(request):
    # 1. Capturamos los parámetros de filtrado desde la URL
    query_cedula = request.GET.get('q', '')
    query_parroquia = request.GET.get('p', '')

    # 2. QuerySet para la TABLA (mantiene el orden cronológico)
    registers = Register.objects.all().order_by('-created_at')

    # Aplicamos filtros a los registros de la tabla
    if query_cedula:
        registers = registers.filter(cedula__icontains=query_cedula)
    
    if query_parroquia:
        registers = registers.filter(parroquia=query_parroquia)

    # 3. Manejo de Exportación Excel (Si se solicita)
    if 'export' in request.GET:
        return export_registers_excel(registers)

    # 4. Lógica del GRÁFICO (Consulta independiente y limpia)
    # IMPORTANTE: .order_by() vacío evita que Django agrupe por 'created_at' 
    # y duplique las etiquetas en el gráfico.
    stats = registers.values('parroquia').annotate(
        total=Count('parroquia')
    ).order_by() 
    
    # Preparamos las listas para Chart.js
    chart_labels = [item['parroquia'] for item in stats]
    chart_data = [item['total'] for item in stats]

    # 5. Lista estática para el selector (Select) del formulario
    parroquias_list = [
        "Antonio Spinetti Dini", "Arias", "Caracciolo Parra Pérez",
        "Domingo Peña", "El Llano", "El Sagrario", "Gonzalo Picón Febres",
        "Jacinto Plaza", "Lasso de la Vega", "Juan Rodríguez Suárez",
        "Mariano Picón Salas", "Milla", "Osuna Rodríguez", "El Morro",
        "Los Nevados"
    ]

    # 6. Construcción del contexto
    context = {
        'registers': registers,          # Datos para la tabla
        'query_cedula': query_cedula,
        'query_parroquia': query_parroquia,
        'parroquias_list': parroquias_list,
        'chart_labels': json.dumps(chart_labels), # Datos limpios para JS
        'chart_data': json.dumps(chart_data),     # Datos limpios para JS
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
        'Nombres', 'Apellidos', 'Cédula', 'Teléfono', 'Parroquia', 
        'Fecha de Registro', 'Fecha de Despacho', 'Cantidad', 'Tamaño', 
        'Visitado', 'Documentos completos'
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
            reg.parroquia,
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
