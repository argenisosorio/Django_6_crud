from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
from .forms import PersonForm
import openpyxl
from django.http import HttpResponse


def home(request):
    """
    Display the home page listing all Person records.
    
    Args:
        request (HttpRequest): The incoming HTTP request
        
    Returns:
        HttpResponse: Rendered template with all Person objects
    """
    people = Person.objects.all()

    if 'export' in request.GET:
        return export_registers_xlsx(registers)

    context = {
        'people': people,
    }
    return render(request, 'person/home.html', context)

def create_person(request):
    """
    Handle Person creation through a form.
    
    GET: Displays an empty form for creating a new Person
    POST: Processes the submitted form and creates a new Person
    
    Args:
        request (HttpRequest): The incoming HTTP request
        
    Returns:
        HttpResponse: Rendered form template (GET) or redirect to home (POST)
    """
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person:home')
    else:
        form = PersonForm()
    
    context = {'form': form}
    return render(request, 'person/create.html', context)

def detail_person(request, pk):
    """
    Display detailed view of a specific Person.
    
    Args:
        request (HttpRequest): The incoming HTTP request
        pk (int): Primary key of the Person to display
        
    Returns:
        HttpResponse: Rendered detail template
    """
    person = get_object_or_404(Person, pk=pk)
    context = {'person': person}
    return render(request, 'person/detail.html', context)

def update_person(request, pk):
    """
    Handle Person updates through a form.
    
    GET: Displays a form pre-populated with Person data
    POST: Processes the submitted form and updates the Person
    
    Args:
        request (HttpRequest): The incoming HTTP request
        pk (int): Primary key of the Person to update
        
    Returns:
        HttpResponse: Rendered form template (GET) or redirect to detail view (POST)
    """
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person:detail', pk=person.pk)
    else:
        form = PersonForm(instance=person)
    
    context = {'form': form, 'person': person}
    return render(request, 'person/update.html', context)

def delete_person(request, pk):
    """
    Handle Person deletion with confirmation.
    
    GET: Displays confirmation page
    POST: Deletes the specified Person
    
    Args:
        request (HttpRequest): The incoming HTTP request
        pk (int): Primary key of the Person to delete
        
    Returns:
        HttpResponse: Rendered confirmation template (GET) or redirect to home (POST)
    """
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person:home')
    
    context = {'person': person}
    return render(request, 'person/delete.html', context)


def export_registers_xlsx(queryset):
    """Función auxiliar para generar el archivo .xlsx"""
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Reporte de Registros"

    # Definir encabezados
    headers = [
        'Nombre',
        'Email',
        'Edad'
    ]
    ws.append(headers)

    # Estilo básico para la cabecera (Opcional pero recomendado)
    for cell in ws[1]:
        cell.font = openpyxl.styles.Font(bold=True)

    # Agregar los datos del QuerySet filtrado
    for reg in queryset:
        ws.append([
            reg.name,
            reg.email,
            reg.age,
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
    response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
    wb.save(response)

    return response
