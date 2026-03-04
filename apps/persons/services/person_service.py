from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from apps.persons.dtos.person_dto import PersonDTO, UpdatePersonDTO
from apps.persons.models.person import Person

"""
Servicio para manejar la lógica de negocio relacionada con la entidad Person.
Este servicio se encarga de realizar las operaciones CRUD utilizando los modelos
de Django y los DTOs para transferir datos entre el controlador y la capa de
datos.
"""


@transaction.atomic
def create_person(person_dto: PersonDTO) -> Person:
    """
    Crear una nueva persona en el sistema.

    Argumentos:
        person_dto: Objeto de transferencia de datos con información de la
        persona.

    Devuelve:
        La instancia de la persona creada.
    """
    person = Person.objects.create(
        name=person_dto.name,
        email=person_dto.email,
        age=person_dto.age
    )
    return person


@transaction.atomic
def update_person(person_id: int, person_dto: UpdatePersonDTO) -> Person:
    """
    Actualizar la información de una persona existente.

    Argumentos:
        person_id: ID de la persona que se va a actualizar
        person_dto: Objeto de transferencia de datos con la información
        actualizada

    Devuelve:
        La instancia de la persona actualizada
    """
    person = get_object_or_404(Person, id=person_id)
    
    # Lisa de campos que se pueden actualizar
    person_fields = ["name", "email", "age"]
    
    for field in person_fields:
        value = getattr(person_dto, field, None)
        # Update only if value is provided (not None and not empty string)
        if value is not None and value != "":
            setattr(person, field, value)
    
    person.save()
    return person


def delete_person(person_id: int) -> None:
    """
    Eliminar una persona del sistema.

    Args:
        person_id: ID de la persona a eliminar
    """
    person = get_object_or_404(Person, id=person_id)
    person.delete()


def get_all_persons() -> list[Person]:
    """
    Recuperar todas las personas de la base de datos.

    Retorna: list[Person]: Lista de todas las personas ordenadas por fecha de
    creación descendente.
    """
    return Person.objects.all().order_by('-created_at')


def get_person(person_id: int) -> Person:
    """
    Recuperar una persona específica por ID.

    Argumentos:
        person_id: ID de la persona a recuperar

    Devuelve:
        La instancia de la persona solicitada
    """
    return get_object_or_404(Person, id=person_id)
