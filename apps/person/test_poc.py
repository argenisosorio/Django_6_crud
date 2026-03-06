import pytest
from django.core.exceptions import ValidationError
from .models import Person

@pytest.fixture
def person():
    # El método fixture se ejecuta para proveer la instancia del modelo a las pruebas que lo requieran
    return Person.objects.create(
        name='Pedro',
        email='[EMAIL_ADDRESS]',
        age=30
    )

@pytest.mark.django_db
def test_person_creation(person):
    # Usamos assert para verificar que la prueba sea correcta, compara valores reales con esperados
    assert person.name == 'Pedro'
    assert person.email == '[EMAIL_ADDRESS]'
    assert person.age == 30

@pytest.mark.django_db
def test_person_str(person):
    assert str(person) == 'Pedro'

def test_negative_age_fails():
    invalid_person = Person(name="Error", email="[EMAIL_ADDRESS]", age=-10)

    # En pytest usamos pytest.raises para verificar que se lance una excepción
    with pytest.raises(ValidationError):
        invalid_person.full_clean()

def test_invalid_email_format_fails():
    invalid_person = Person(name="Error", email="esto_no_es_un_correo", age=20)

    with pytest.raises(ValidationError):
        invalid_person.full_clean()

def test_name_too_long_fails():
    nombre_largo = "A" * 101
    invalid_person = Person(name=nombre_largo, email="[EMAIL_ADDRESS]", age=25)

    with pytest.raises(ValidationError):
        invalid_person.full_clean()
