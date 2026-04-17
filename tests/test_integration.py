import pytest
from django.urls import reverse
from django.core import mail
from apps.person.models import Person
from apps.product.models import Product

@pytest.mark.django_db
class TestIntegration:

    def setup_method(self):
        # Creamos un producto de prueba
        self.product = Product.objects.create(name="Producto de prueba", price=100)

    def test_template_view_model_communication(self, client):
        """
        Prueba 1: Cómo se comunica la Template (HTML), la Vista (View) y el Modelo (Database).
        Verifica que la vista lista recupere el modelo correctamente y use el template adecuado.
        """
        # Crear un registro en la BD
        Person.objects.create(name="Usuario Test", email="test@example.com", age=25, product=self.product)
        
        # Obtener la url del listado de personas
        url = reverse('person:home')
        response = client.get(url)
        
        # Verificar comunicación View -> Template
        assert response.status_code == 200
        assert 'person/home.html' in [t.name for t in response.templates]
        
        # Verificar comunicación Modelo -> View -> Template (Contexto)
        assert 'people' in response.context
        assert len(response.context['people']) == 1
        assert response.context['people'][0].name == "Usuario Test"

    def test_view_model_database_interaction(self, client):
        """
        Prueba 2: Cómo interactúa la vista View con el Modelo y la Base de Datos.
        Verifica que al hacer un POST a la vista, el modelo guarda la información en la BD.
        """
        url = reverse('person:create')
        data = {
            'name': 'Nuevo Usuario DB',
            'email': 'nuevo@example.com',
            'age': 30,
            'product': self.product.id
        }
        
        # La vista interactúa con el form y el modelo para guardar
        response = client.post(url, data)
        
        # Si se creó con éxito, debería redirigir
        assert response.status_code == 302
        
        # Verificar que la Base de Datos se actualizó usando el modelo
        assert Person.objects.filter(name='Nuevo Usuario DB').exists()
        person = Person.objects.get(name='Nuevo Usuario DB')
        assert person.age == 30

    def test_external_services_email(self, client):
        """
        Prueba 3: Comportamiento de servicios externos (envío de correos).
        Verifica que se envíe un correo al crear una persona con el correo especificado.
        """
        url = reverse('person:create')
        target_email = "tucorreo@example.com"
        data = {
            'name': 'Usuario Correo',
            'email': target_email,
            'age': 20,
            'product': self.product.id
        }
        
        # Vaciar outbox por si acaso
        mail.outbox = []
        
        # El POST disparará el envío de correo en la vista
        response = client.post(url, data)
        
        assert response.status_code == 302
        
        # Comprobar directamente el comportamiento del servicio de correo interceptado por Django
        assert len(mail.outbox) == 1
        sent_email = mail.outbox[0]
        assert sent_email.subject == "¡Bienvenido a nuestro sistema!"
        assert target_email in sent_email.to
        # Verificamos que contenga contenido extraído del template html
        assert "Usuario Correo" in sent_email.body or "Usuario Correo" in sent_email.alternatives[0][0]

    def test_model_relationship_person_product(self):
        """
        Prueba 4: Crear una relación y verificar cómo se comporta entre Person y Product.
        """
        # Crear un producto (ya tenemos self.product)
        product2 = Product.objects.create(name="Laptop", price=1500)
        
        # Crear la persona asignando el producto para probar la relación Foránea (One-To-Many en sentido inverso)
        person = Person.objects.create(
            name="Comprador",
            email="comprador@example.com",
            age=35,
            product=product2
        )
        
        # Verificar cómo se comporta la relación
        # 1. Desde Person hacia Product
        assert person.product == product2
        assert person.product.name == "Laptop"
        assert person.product.price == 1500
        
        # 2. Desde Product hacia Person (related_name='persons')
        assert product2.persons.count() == 1
        assert product2.persons.first() == person
