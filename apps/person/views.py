from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
from .forms import PersonForm
from auditlog.models import LogEntry
from django.contrib.contenttypes.models import ContentType


def home(request):
    """
    Display the home page listing all Person records.
    
    Args:
        request (HttpRequest): The incoming HTTP request
        
    Returns:
        HttpResponse: Rendered template with all Person objects
    """
    people = Person.objects.all()
    context = {
        'people': people,
        'message': '¡Hello Django 6 Person CRUD!',
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


def person_audit_log(request):
    """
    Display audit logs for the Person model.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered template with audit logs
    """
    # Get the content type for the Person model.
    person_ct = ContentType.objects.get_for_model(Person)

    # Get all log entries for the Person model, ordered by timestamp (newest first)
    logs = LogEntry.objects.filter(content_type=person_ct).order_by('-timestamp')

    # Create context with the logs
    context = {
        'logs': logs
    }

    # Render the audit log template
    return render(request, 'person/audit_log.html', context)
