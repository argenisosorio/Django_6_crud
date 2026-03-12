import pytest
from django.core.exceptions import ValidationError
from .models import Person

"""
Definimos un fixture que se ejecutará para proveer la instancia a las pruebas
que lo requieran como argumento (la función se llama "person" y devuelve una
instancia de Person creada en la base de datos).
"""
@pytest.fixture
def person():
    return Person.objects.create(
        name='Pedro',
        email='[EMAIL_ADDRESS]',
        age=30
    )

"""
Los métodos de prueba también deben comenzar o terminar con "test", odemos pedir
la instancia de Person usando el argumento "person" que equivale a nuestro
fixture y se usa @pytest.mark.django_db en pruebas que requieran acceso a la
base de datos
"""
@pytest.mark.django_db
# Para el caso de un test de afirmación.
def test_person_creation(person):
    # En pytest usamos el assert nativo de Python para verificar la validez.
    assert person.name == 'Pedro'
    assert person.email == '[EMAIL_ADDRESS]'
    assert person.age == 30

"""
Usamos pytest.raises para capturar excepciones esperadas (ValidationError en
este caso) para el caso de un test de excepción
"""
def test_negative_age_fails():
    """
    Verifica que la validación de edad negativa falle correctamente.
    """
    invalid_person = Person(name="Error", email="[EMAIL_ADDRESS]", age=-10)

    """
    Se espera que al llamar a full_clean() se lance una ValidationError debido a
    la edad negativa.
    """
    with pytest.raises(ValidationError):
        invalid_person.full_clean()
