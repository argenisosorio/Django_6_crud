# Django 6 CRUD Example + Bootstrap 5

The following is an example of CRUD (Create, Read, Update, Delete) in Django 6.

There are 2 CRUD applications, one uses function-based views (FBV) and the other
uses class-based views (CBV).

## Requirements:
```
Django==6.0.2
Python>=3.12
```

## Run the following commands in sequence to deploy the project to a development environment:

```bash
Creating a Python 3 virtual environment:

1. Update the package list:

$ sudo apt update

2. Install python3-venv

$ sudo apt install python3-venv

3. Create the virtual environment:

$ python3 -m venv my_environment

4. Activate the environment:

$ source my_environment/bin/activate
```

Now install de Requirements

```bash
$ pip install -r requirements.txt

$ cp Django_6_crud/settings.py_example Django_6_crud/settings.py

$ python manage.py makemigrations person product

$ python manage.py migrate

$ python manage.py runserver
```

## Test the project:

Open your browser to http://127.0.0.1:8000 and you'll see the Django 6 CRUD
application for managing people records.

## Image

![1.png](1.png "1.png")

![2.png](2.png "2.png")

![3.png](3.png "3.png")

![4.png](4.png "4.png")

## Realizar Pruebas de Integración

Las pruebas de integración en este proyecto tienen como objetivo validar que los distintos módulos de la aplicación (Modelos, Vistas, Templates y Servicios Externos) trabajen en conjunto correctamente. A diferencia de las pruebas unitarias, aquí no probamos una función aislada, sino el flujo de datos a través de las diferentes capas de la arquitectura Django.

### 1. Requisitos previos e Importaciones
Para ejecutar estas pruebas, utilizamos el cliente de pruebas de Django (`client`) inyectado por `pytest-django`. Este cliente actúa como un navegador web simulado.

```python
import pytest
from django.urls import reverse
from django.core import mail
from apps.person.models import Person
from apps.product.models import Product
```

### 2. Estructura de la Clase de Integración
Utilizamos la marca `@pytest.mark.django_db` para permitir el acceso a la base de datos de prueba. En el método `setup_method`, preparamos los datos base necesarios para cada test.

```python
@pytest.mark.django_db
class TestIntegration:
    def setup_method(self):
        # Creamos un producto de prueba base para todas las integraciones
        self.product = Product.objects.create(name="Producto de prueba", price=100)
```

### 3. Ejecución de Pruebas de Integración Paso a Paso

#### A. Comunicación Template - Vista - Modelo
Esta prueba verifica que la Vista sea capaz de recuperar datos del Modelo y enviarlos correctamente al Template (HTML) a través del contexto.

Archivo de prueba: `test_template_view_model_communication`
¿Qué prueba?: Valida el código de estado HTTP (200), que el template usado sea el correcto y que el objeto creado en la BD aparezca en el contexto de la vista.

```python
    def test_template_view_model_communication(self, client):
        # 1. Crear un registro real en la BD
        Person.objects.create(name="Usuario Test", email="test@example.com", age=25, product=self.product)
        
        # 2. Obtener la URL por nombre (reverse)
        url = reverse('person:home')
        response = client.get(url)
        
        # 3. Verificar que la vista cargó el template esperado
        assert response.status_code == 200
        assert 'person/home.html' in [t.name for t in response.templates]
        
        # 4. Verificar que los datos del Modelo fluyeron hasta el Template
        assert 'people' in response.context
        assert response.context['people'][0].name == "Usuario Test"
```

#### B. Interacción Vista - Modelo - Base de Datos
Aquí validamos el proceso de escritura. Verificamos que al enviar un formulario (POST), la Vista procese la información y el Modelo la persista realmente en la Base de Datos.

Archivo de prueba: `test_view_model_database_interaction`
¿Qué prueba?: La redirección tras el guardado (302) y la existencia física del nuevo registro en la base de datos con los valores correctos.

```python
    def test_view_model_database_interaction(self, client):
        url = reverse('person:create')
        data = {
            'name': 'Nuevo Usuario DB',
            'email': 'nuevo@example.com',
            'age': 30,
            'product': self.product.id
        }
        
        # Simular envío de formulario
        response = client.post(url, data)
        
        # Verificar persistencia en Base de Datos
        assert response.status_code == 302
        assert Person.objects.filter(name='Nuevo Usuario DB').exists()
        
        person = Person.objects.get(name='Nuevo Usuario DB')
        assert person.age == 30
```

#### C. Integración con Servicios Externos (Emails)
En sistemas de donación, es vital que las notificaciones funcionen. Django intercepta los correos salientes y los almacena en `mail.outbox` durante las pruebas.

Archivo de prueba: `test_external_services_email`
¿Qué prueba?: Que el envío de correo se dispare tras una acción y que el destinatario y el asunto coincidan con lo programado.

```python
    def test_external_services_email(self, client):
        url = reverse('person:create')
        target_email = "tucorreo@example.com"
        data = { 'name': 'Usuario Correo', 'email': target_email, 'age': 20, 'product': self.product.id }
        
        # Limpiar bandeja de salida simulada
        mail.outbox = []
        
        # Ejecutar acción que dispara el correo
        client.post(url, data)
        
        # Verificar comportamiento del servicio de correo
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == "¡Bienvenido a nuestro sistema!"
        assert target_email in mail.outbox[0].to
```

#### D. Integración de Relaciones entre Modelos
Esta prueba valida la integridad referencial y cómo se comportan las relaciones `ForeignKey` entre la persona y el producto (donación/compra).

Archivo de prueba: `test_model_relationship_person_product`
¿Qué prueba?: La navegación en ambos sentidos de la relación (de Person a Product y viceversa usando `related_name`).

```python
    def test_model_relationship_person_product(self):
        product2 = Product.objects.create(name="Laptop", price=1500)
        person = Person.objects.create(name="Comprador", email="comp@ex.com", age=35, product=product2)
        
        # Probar relación directa (Person -> Product)
        assert person.product.name == "Laptop"
        
        # Probar relación inversa (Product -> Person) usando el manager 'persons'
        assert product2.persons.count() == 1
        assert product2.persons.first() == person
```

### 4. Comando para ejecutar las pruebas de Integración
Al igual que con las unitarias, puedes ejecutar este archivo específico para validar la integración de los componentes:

```bash
pytest tests/test_integration.py
```

