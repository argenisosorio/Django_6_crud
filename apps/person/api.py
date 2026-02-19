from ninja import Router, ModelSchema, Schema
from django.shortcuts import get_object_or_404
from typing import List
from .models import Person

router = Router()

# --- SCHEMAS ---

class PersonSchema(ModelSchema):
    """Schema basado en el modelo para devolver datos (Output)"""
    class Meta:
        model = Person
        fields = ['id', 'name', 'email', 'age', 'created_at', 'updated_at']

class PersonCreateSchema(Schema):
    """Schema para recibir datos al crear o actualizar (Input)"""
    name: str
    email: str
    age: int

# --- ENDPOINTS (CRUD) ---

# 1. Listar personas (GET)
@router.get("/", response=List[PersonSchema])
def list_people(request):
    return Person.objects.all()

# 2. Obtener una persona (GET por ID)
@router.get("/{person_id}", response=PersonSchema)
def get_person(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    return person

# 3. Crear una persona (POST)
@router.post("/", response=PersonSchema)
def create_person(request, data: PersonCreateSchema):
    # .dict() convierte el esquema de Pydantic en un diccionario de Python
    person = Person.objects.create(**data.dict())
    return person

# 4. Actualizar una persona (PUT)
@router.put("/{person_id}", response=PersonSchema)
def update_person(request, person_id: int, data: PersonCreateSchema):
    person = get_object_or_404(Person, id=person_id)
    for attr, value in data.dict().items():
        setattr(person, attr, value)
    person.save()
    return person

# 5. Eliminar una persona
@router.delete("/{person_id}")
def delete_person(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return {"success": True, "message": f"Person {person_id} deleted successfully"}
