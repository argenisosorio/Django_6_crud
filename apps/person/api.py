from typing import List
from django import forms
from django.shortcuts import get_object_or_404
from ninja import Router, ModelSchema, Schema
from .models import Person

router = Router()

# --- DJANGO FORMS (Para validaciones de negocio) ---

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['name', 'email', 'age']

# --- SCHEMAS (Ninja/Pydantic) ---

class PersonSchema(ModelSchema):
    """Esquema para devolver datos (Output)"""
    class Meta:
        model = Person
        fields = ['id', 'name', 'email', 'age', 'created_at', 'updated_at']

class PersonCreateSchema(Schema):
    """Esquema para recibir datos (Input)"""
    name: str
    email: str
    age: int

class ErrorSchema(Schema):
    """Esquema para estructurar los errores de validación"""
    errors: dict

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
@router.post("/", response={201: PersonSchema, 400: ErrorSchema})
def create_person(request, data: PersonCreateSchema):
    # Pasamos los datos del Schema al Form de Django
    form = PersonForm(data.dict())

    if form.is_valid():
        person = form.save()
        return 201, person

    # Si falla, devolvemos los errores en formato JSON
    return 400, {"errors": form.errors.get_json_data()}

# 4. Actualizar una persona (PUT)
@router.put("/{person_id}", response={200: PersonSchema, 400: ErrorSchema})
def update_person(request, person_id: int, data: PersonCreateSchema):
    person = get_object_or_404(Person, id=person_id)

    # Vinculamos el formulario a la instancia existente
    form = PersonForm(data.dict(), instance=person)

    if form.is_valid():
        person = form.save()
        return 200, person

    return 400, {"errors": form.errors.get_json_data()}

# 5. Eliminar una persona (DELETE)
@router.delete("/{person_id}")
def delete_person(request, person_id: int):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return {"success": True, "message": f"Person {person_id} deleted successfully"}
