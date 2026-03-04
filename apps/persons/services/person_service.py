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
    Create a new person in the system.
    
    Args:
        person_dto: Data transfer object with person information
        
    Returns:
        Person: The created person instance
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
    Update an existing person's information.
    
    Args:
        person_id: ID of the person to update
        person_dto: Data transfer object with updated information
        
    Returns:
        Person: The updated person instance
    """
    person = get_object_or_404(Person, id=person_id)
    
    # List of fields that can be updated
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
    Delete a person from the system.
    
    Args:
        person_id: ID of the person to delete
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
    Retrieve a specific person by ID.
    
    Args:
        person_id: ID of the person to retrieve
        
    Returns:
        Person: The requested person instance
    """
    return get_object_or_404(Person, id=person_id)
