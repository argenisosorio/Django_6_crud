# tests/test_integration.py
"""
Pruebas de integración para el CRUD de Person.

Verifica la interacción correcta entre:
- Vistas (views.py)
- Modelo (Person)
- Formulario (PersonForm)
- Base de datos
- Templates
"""

import pytest
from django.urls import reverse
from django.test import Client
from apps.person.models import Person
from apps.person.forms import PersonForm


pytestmark = pytest.mark.django_db


class TestPersonCRUDIntegration:
    """
    Suite de pruebas de integración para el CRUD completo de Person.
    Verifica flujos completos desde la vista hasta la base de datos.
    """

    # =========================================================================
    # Fixtures de prueba
    # =========================================================================

    @pytest.fixture
    def client(self):
        """
        Fixture que retorna un cliente Django para realizar peticiones HTTP.

        Returns:
            Client: Cliente Django no autenticado.
        """
        return Client()

    @pytest.fixture
    def sample_person_data(self):
        """
        Fixture con datos de ejemplo para crear una persona.

        Returns:
            dict: Datos válidos para crear una instancia de Person.
        """
        return {
            'name': 'Juan Pérez',
            'email': 'juan@example.com',
            'age': 30,
        }

    @pytest.fixture
    def existing_person(self, sample_person_data):
        """
        Fixture que crea y retorna una persona existente en BD.

        Args:
            sample_person_data: Datos de la persona a crear.

        Returns:
            Person: Instancia de Person guardada en la base de datos.
        """
        return Person.objects.create(**sample_person_data)

    # =========================================================================
    # Prueba de integración: Creación completa de Person
    # =========================================================================

    def test_full_create_person_flow(self, client, sample_person_data):
        """
        Prueba el flujo completo de creación de una persona:

        1. GET a la página de creación (verifica formulario)
        2. POST con datos válidos
        3. Verifica redirección
        4. Verifica que los datos persisten en BD
        5. Verifica que la persona aparece en el listado

        Args:
            client: Cliente Django.
            sample_person_data: Datos de prueba para la persona.
        """
        # 1. Verificar que el formulario de creación se carga correctamente
        create_url = reverse('person:create')
        get_response = client.get(create_url)
        assert get_response.status_code == 200
        assert b'form' in get_response.content.lower()

        # 2. Enviar solicitud POST con datos válidos
        post_response = client.post(create_url, sample_person_data)

        # 3. Verificar redirección después de crear
        assert post_response.status_code == 302
        assert post_response.url == reverse('person:home')

        # 4. Verificar que la persona existe en la base de datos
        person = Person.objects.get(email=sample_person_data['email'])
        assert person.name == sample_person_data['name']
        assert person.age == sample_person_data['age']

        # 5. Verificar que la persona aparece en el listado
        home_response = client.get(reverse('person:home'))
        assert home_response.status_code == 200
        assert sample_person_data['name'].encode() in home_response.content

    # =========================================================================
    # Prueba de integración: Lectura (Listado y Detalle)
    # =========================================================================

    def test_full_read_person_flow(self, client, existing_person):
        """
        Prueba el flujo completo de lectura de una persona:

        1. Accede al listado (home)
        2. Verifica que la persona aparece
        3. Accede al detalle de la persona
        4. Verifica que los datos coinciden

        Args:
            client: Cliente Django.
            existing_person: Persona previamente creada en BD.
        """
        # 1. Acceder al listado principal
        home_url = reverse('person:home')
        home_response = client.get(home_url)
        assert home_response.status_code == 200

        # 2. Verificar que la persona aparece en el listado
        assert existing_person.name.encode() in home_response.content
        assert str(existing_person.age).encode() in home_response.content

        # 3. Acceder al detalle de la persona
        detail_url = reverse('person:detail', args=[existing_person.pk])
        detail_response = client.get(detail_url)
        assert detail_response.status_code == 200

        # 4. Verificar que los datos del detalle coinciden
        assert existing_person.name.encode() in detail_response.content
        assert existing_person.email.encode() in detail_response.content
        assert str(existing_person.age).encode() in detail_response.content

    # =========================================================================
    # Prueba de integración: Actualización de Person
    # =========================================================================

    def test_full_update_person_flow(self, client, existing_person):
        """
        Prueba el flujo completo de actualización de una persona:

        1. GET a la página de edición (verifica datos precargados)
        2. POST con datos modificados
        3. Verifica redirección al detalle
        4. Verifica que los cambios persisten en BD
        5. Verifica que los cambios se reflejan en el listado

        Args:
            client: Cliente Django.
            existing_person: Persona previamente creada en BD.
        """
        updated_data = {
            'name': 'Juan Pérez Actualizado',
            'email': 'juan.actualizado@example.com',
            'age': 35,
        }

        # 1. Verificar que el formulario de edición carga con datos precargados
        update_url = reverse('person:update', args=[existing_person.pk])
        get_response = client.get(update_url)
        assert get_response.status_code == 200
        assert existing_person.name.encode() in get_response.content

        # 2. Enviar solicitud POST con datos actualizados
        post_response = client.post(update_url, updated_data)

        # 3. Verificar redirección al detalle después de actualizar
        assert post_response.status_code == 302
        assert post_response.url == reverse('person:detail', args=[existing_person.pk])

        # 4. Verificar que los cambios persisten en la base de datos
        person_refreshed = Person.objects.get(pk=existing_person.pk)
        assert person_refreshed.name == updated_data['name']
        assert person_refreshed.email == updated_data['email']
        assert person_refreshed.age == updated_data['age']

        # 5. Verificar que los cambios se reflejan en el listado
        home_response = client.get(reverse('person:home'))
        assert home_response.status_code == 200
        assert updated_data['name'].encode() in home_response.content

    # =========================================================================
    # Prueba de integración: Eliminación de Person
    # =========================================================================

    def test_full_delete_person_flow(self, client, existing_person):
        """
        Prueba el flujo completo de eliminación de una persona:

        1. GET a la página de confirmación
        2. Verifica que la persona existe en BD
        3. POST confirmando eliminación
        4. Verifica redirección al listado
        5. Verifica que la persona ya no existe en BD
        6. Verifica que la persona ya no aparece en el listado

        Args:
            client: Cliente Django.
            existing_person: Persona previamente creada en BD.
        """
        person_id = existing_person.pk
        person_name = existing_person.name

        # 1. Verificar que la página de confirmación de eliminación se carga
        delete_url = reverse('person:delete', args=[person_id])
        get_response = client.get(delete_url)
        assert get_response.status_code == 200
        assert person_name.encode() in get_response.content

        # 2. Verificar que la persona existe en la base de datos antes de eliminar
        assert Person.objects.filter(pk=person_id).exists() is True

        # 3. Enviar solicitud POST confirmando eliminación
        post_response = client.post(delete_url)

        # 4. Verificar redirección al listado después de eliminar
        assert post_response.status_code == 302
        assert post_response.url == reverse('person:home')

        # 5. Verificar que la persona ya no existe en la base de datos
        assert Person.objects.filter(pk=person_id).exists() is False

        # 6. Verificar que la persona ya no aparece en el listado
        home_response = client.get(reverse('person:home'))
        assert home_response.status_code == 200
        assert person_name.encode() not in home_response.content

    # =========================================================================
    # Prueba de integración: Validación de formulario
    # =========================================================================

    def test_form_validation_integration(self, client):
        """
        Prueba que la validación del formulario funciona correctamente
        en el flujo de creación:

        1. POST con datos inválidos (edad negativa)
        2. Verifica que NO redirige (vuelve al mismo formulario)
        3. Verifica que NO se crea un registro en BD
        4. Verifica que el formulario muestra errores

        Args:
            client: Cliente Django.
        """
        invalid_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'age': -5,  # Edad inválida (negativa)
        }

        create_url = reverse('person:create')

        # 1. Enviar datos inválidos
        response = client.post(create_url, invalid_data)

        # 2. Verificar que NO hay redirección (status 200 = vuelve al formulario)
        assert response.status_code == 200

        # 3. Verificar que NO se creó ningún registro en la base de datos
        assert Person.objects.filter(email=invalid_data['email']).exists() is False

        # 4. Verificar que el formulario muestra errores en el template
        assert b'error' in response.content.lower() or b'valid' in response.content.lower()

    # =========================================================================
    # Prueba de integración: Manejo de errores 404
    # =========================================================================

    def test_404_error_handling_integration(self, client):
        """
        Prueba que las vistas manejan correctamente IDs inexistentes:

        1. Accede al detalle de una persona que no existe
        2. Verifica que retorna 404
        3. Accede a edición de persona inexistente
        4. Verifica que retorna 404
        5. Accede a eliminación de persona inexistente
        6. Verifica que retorna 404

        Args:
            client: Cliente Django.
        """
        non_existent_id = 99999

        # 1. Verificar detalle de persona inexistente
        detail_url = reverse('person:detail', args=[non_existent_id])
        detail_response = client.get(detail_url)
        assert detail_response.status_code == 404

        # 2. Verificar edición de persona inexistente
        update_url = reverse('person:update', args=[non_existent_id])
        update_response = client.get(update_url)
        assert update_response.status_code == 404

        # 3. Verificar eliminación de persona inexistente
        delete_url = reverse('person:delete', args=[non_existent_id])
        delete_response = client.get(delete_url)
        assert delete_response.status_code == 404

    # =========================================================================
    # Prueba de integración: Redirecciones y flujos completos
    # =========================================================================

    def test_complete_crud_workflow(self, client):
        """
        Prueba el flujo CRUD completo de extremo a extremo:

        1. Crear una persona
        2. Listar personas (verificar que aparece)
        3. Ver detalle
        4. Actualizar datos
        5. Verificar cambios en detalle y listado
        6. Eliminar persona
        7. Verificar que desaparece del listado

        Args:
            client: Cliente Django.
        """
        # Datos iniciales
        initial_data = {
            'name': 'María López',
            'email': 'maria@example.com',
            'age': 28,
        }

        create_url = reverse('person:create')

        # 1. Crear persona
        post_response = client.post(create_url, initial_data)
        assert post_response.status_code == 302

        # Obtener la persona recién creada
        person = Person.objects.get(email=initial_data['email'])
        assert person.name == initial_data['name']

        # 2. Verificar que aparece en el listado
        home_response = client.get(reverse('person:home'))
        assert initial_data['name'].encode() in home_response.content

        # 3. Ver detalle
        detail_url = reverse('person:detail', args=[person.pk])
        detail_response = client.get(detail_url)
        assert initial_data['email'].encode() in detail_response.content

        # 4. Actualizar datos
        updated_data = {
            'name': 'María López Actualizada',
            'email': 'maria.actualizada@example.com',
            'age': 29,
        }
        update_url = reverse('person:update', args=[person.pk])
        update_response = client.post(update_url, updated_data)
        assert update_response.status_code == 302

        # 5. Verificar cambios
        person.refresh_from_db()
        assert person.name == updated_data['name']
        assert person.email == updated_data['email']
        assert person.age == updated_data['age']

        # Verificar cambios en detalle
        detail_response = client.get(detail_url)
        assert updated_data['name'].encode() in detail_response.content
        assert updated_data['email'].encode() in detail_response.content

        # Verificar cambios en listado
        home_response = client.get(reverse('person:home'))
        assert updated_data['name'].encode() in home_response.content

        # 6. Eliminar persona
        delete_url = reverse('person:delete', args=[person.pk])
        delete_response = client.post(delete_url)
        assert delete_response.status_code == 302

        # 7. Verificar que desapareció del listado
        home_response = client.get(reverse('person:home'))
        assert updated_data['name'].encode() not in home_response.content

        # Verificar que ya no existe en BD
        assert Person.objects.filter(pk=person.pk).exists() is False
