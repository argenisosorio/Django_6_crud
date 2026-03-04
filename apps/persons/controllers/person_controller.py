from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_POST
from apps.persons.dtos.person_dto import PersonDTO, UpdatePersonDTO
from apps.persons.models.person import Person
from apps.persons.requests.create_person import CreatePersonRequest
from apps.persons.requests.update_person import UpdatePersonRequest
from apps.persons.services import person_service


"""
Controlador para manejar las operaciones CRUD relacionadas con la entidad Person.
Este controlador se encarga de recibir las solicitudes HTTP, interactuar con el
servicio de personas y devolver las respuestas adecuadas.
"""


"""
Vista para mostrar la lista de personas, recupera todas las personas
utilizando el servicio correspondiente y las pasa al template para su
renderizado.
"""
def index(request):
    persons = person_service.get_all_persons()
    context = {"persons": persons}
    return render(request, "persons/index.html", context)


"""
Vista para mostrar el formulario de creación de una nueva persona.
"""
@require_GET
def create(request: HttpRequest) -> HttpResponse:
    return render(request, "persons/create_person.html")


"""
Vista para mostrar el formulario de edición de una persona existente.
"""
@require_GET
def edit(request: HttpRequest, person_id: int) -> HttpResponse:
    person = person_service.get_person(person_id)
    context = {"person": person}
    return render(request, "persons/update.html", context)


"""
Vista para manejar la creación de una nueva persona. Valida los datos recibidos
y, si son válidos, crea la persona utilizando el servicio correspondiente.
"""
@require_POST
def store(request: HttpRequest) -> HttpResponse:
    # Formulario para validar los datos de entrada y crear un DTO para el servicio
    form = CreatePersonRequest(request.POST)

    # Si los datos no son válidos, devolver un error con los mensajes de validación
    if not form.is_valid():
        return HttpResponse(f"Invalid data: {form.errors}", status=400)

    """
    Crear un DTO a partir de los datos validados y llamar al servicio para crear
    la persona
    """
    person_dto = PersonDTO(**form.cleaned_data)
    person_service.create_person(person_dto)
    return redirect(reverse("persons:index"))


"""
Vista para manejar la eliminación de una persona. Recibe el ID de la persona a
eliminar y utiliza el servicio correspondiente para eliminarla del sistema.
"""
@require_POST
def delete(request: HttpRequest, person_id: int) -> HttpResponse:
    person_service.delete_person(person_id)
    return redirect(reverse("persons:index"))


"""
Vista para manejar la actualización de una persona existente. Valida los datos
recibidos y, si son válidos, actualiza la persona utilizando el servicio
correspondiente.
"""
@require_POST   
def update(request: HttpRequest, person_id: int) -> HttpResponse:
    person_data = UpdatePersonRequest(request.POST)
    if not person_data.is_valid():
        return HttpResponse(f"Invalid data: {person_data.errors}", status=400)

    person_dto = UpdatePersonDTO(**person_data.cleaned_data)
    person_service.update_person(person_id, person_dto)
    return redirect(reverse("persons:index"))
