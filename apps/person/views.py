from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
from .forms import PersonForm
from django.core.mail import send_mail
from django.conf import settings


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
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            # 1. Guardamos el objeto y lo asignamos a una variable
            person = form.save()

            # 2. Enviamos el correo
            send_mail(
                subject="¡Bienvenido a nuestro sistema!",
                message=f"Hola {person.name}, tu registro ha sido exitoso.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[person.email],
                fail_silently=False, # Ponlo en True en producción si no quieres que la web falle si el mail falla
            )
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
