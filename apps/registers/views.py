from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Register
from .forms import RegisterForm
import openpyxl
from django.http import HttpResponse


@login_required
def home(request):
    # 1. Capturamos los parámetros de filtrado
    query_cedula = request.GET.get('q', '')
    query_parroquia = request.GET.get('p', '')

    # 2. QuerySet base
    registers = Register.objects.all().order_by('-created_at')

    # 3. Aplicamos filtros encadenados
    if query_cedula:
        registers = registers.filter(cedula__icontains=query_cedula)
    
    if query_parroquia:
        registers = registers.filter(parroquia=query_parroquia)

    # 4. Manejo de Exportación Excel (Detectamos si se pide el archivo)
    if 'export' in request.GET:
        return export_registers_excel(registers)

    parroquias_list = [
        "Antonio Spinetti Dini", "Arias", "Caracciolo Parra Pérez",
        "Domingo Peña", "El Llano", "El Sagrario", "Gonzalo Picón Febres",
        "Jacinto Plaza", "Lasso de la Vega", "Juan Rodríguez Suárez",
        "Mariano Picón Salas", "Milla", "Osuna Rodríguez", "El Morro",
        "Los Nevados"
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
