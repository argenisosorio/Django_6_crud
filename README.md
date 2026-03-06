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

## Realizar Pruebas Unitarias

### unittest

Para realizar pruebas unitarias en Django, podemos usar el módulo unittest, que es un módulo de Python para crear pruebas unitarias. No es necesario instalarlo.

Para utilizarlo debemos modificar el archivo test.py de la aplicación que queremos probar.
Donde inicialmente debemos importar el Modelo a probar, las clases `TestCase` y `ValidationError`.

```python
from django.test import TestCase
from .models import Person
from django.core.exceptions import ValidationError
```

`TestCase` es una clase que se utiliza para crear pruebas unitarias, y `ValidationError` es una clase que se utiliza para validar los datos del modelo.

Luego debemos definir una clase que herede de `TestCase` y definir los métodos de prueba.

Antes debemos tener en cuenta que existen pruebas de afirmación y pruebas de excepción, donde las de afirmación determinan un flujo ideal y las de excepción
buscan explotar de alguna forma, para eso usamos `ValidationError`.

```python
class PersonModelTest(TestCase):
    # El método setUp se ejecuta antes de cada prueba y es el que nos permite crear una instancia del modelo
    def setUp(self):
        self.person = Person.objects.create(
            name='Pedro',
            email='[EMAIL_ADDRESS]',
            age=30
        )

    # Los métodos de prueba deben comenzar con "test_"
    # En este caso será un test de afirmación
    # Podemos añadir un docstring para describir la prueba (Es el texto que se encuentra entre """)
    # Y debemos usar self.assert* para verificar que la prueba sea correcta, compara valores reales
    # con valores esperados
    def test_person_creation(self):
        """🟦 Verifica que la persona se cree correctamente"""
        self.assertEqual(self.person.name, 'Pedro')
        self.assertEqual(self.person.email, '[EMAIL_ADDRESS]')
        self.assertEqual(self.person.age, 30)

    # En este caso será un test de excepcion (se usa ValidationError)
    # y usamos assertRaises para verificar que se lance una ValidationError
    # full_clean() es un método que valida el modelo
    def test_negative_age_fails(self):
        """🟦 Verifica que no se permitan edades negativas"""
        invalid_person = Person(name="Error", email="[EMAIL_ADDRESS]", age=-10)

        with self.assertRaises(ValidationError):
            invalid_person.full_clean()

    
```
Aquí hemos definido una prueba que verifica que la persona se cree correctamente.

¿Cómo ejecutamos las pruebas que hemos creado?

Para ejecutar todos los tests de una app debemos ejecutar el siguiente comando:

```bash
$ python manage.py test apps.myapp.tests
```
Debería mostrar algo como:

```
Creating test database for alias 'default'...

----------------------------------------------------------------------
Ran 1 tests in 0.002s

OK
Destroying test database for alias 'default'...
```

O podemos ejecutar una prueba específica con el siguiente comando:

```bash
$ python manage.py test apps.myapp.tests.MyModelModelTest.test_my_model_creation
```

Si queremos información detallada de las pruebas que se están ejecutando junto con el docstring que indicamos en cada prueba debemos añadir el flag -v 2 al comando, por ejemplo:

```bash
$ python manage.py test apps.myapp.tests -v 2
```

### pytest

Otra alternativa más moderna y menos rígida para realizar pruebas unitarias en Django, es usar pytest, que es un framework de pruebas para Python.

Inicialmente se debe instalar pytest-django con el siguiente comando:

```bash
$ pip install pytest pytest-django
```

Debemos configurar pytest en el archivo `pytest.ini` en la raíz de tu proyecto:

```ini
[pytest]
# Indica el archivo de configuración de Django en tu proyecto
DJANGO_SETTINGS_MODULE = Django_6_crud.settings
# Indica los archivos que se considerarán como pruebas
python_files = tests.py test_*.py *_tests.py
```

Para utilizarlo debemos crear o modificar un archivo de pruebas (por ejemplo `test_poc.py`) en nuestra aplicación.
A diferencia de `unittest`, con `pytest` no estamos obligados a definir una clase. Podemos definir simples funciones y hacer uso de *fixtures* para la preparación de los datos:

```python
import pytest
from django.core.exceptions import ValidationError
from .models import Person

# Definimos un fixture que se ejecutará para proveer la instancia a las pruebas que lo requieran como argumento
@pytest.fixture
def person():
    return Person.objects.create(
        name='Pedro',
        email='[EMAIL_ADDRESS]',
        age=30
    )

# Los métodos de prueba también deben comenzar o terminar con "test"
# Podemos pedir la instancia de Person usando el argumento "person" que equivale a nuestro fixture
# y se usa @pytest.mark.django_db en pruebas que requieran acceso a la base de datos
@pytest.mark.django_db
# Para el caso de un test de afirmación
def test_person_creation(person):
    # En pytest usamos el assert nativo de Python para verificar la validez
    assert person.name == 'Pedro'
    assert person.email == '[EMAIL_ADDRESS]'
    assert person.age == 30

# Usamos pytest.raises para capturar excepciones esperadas (ValidationError en este caso)
# Para el caso de un test de excepción
def test_negative_age_fails():
    invalid_person = Person(name="Error", email="[EMAIL_ADDRESS]", age=-10)

    with pytest.raises(ValidationError):
        invalid_person.full_clean()
```
Aquí hemos definido pruebas idénticas a la versión de unittest aprovechando todo el potencial de pytest.

¿Cómo ejecutamos las pruebas con pytest?

Para ejecutar todos los tests de nuestro proyecto usando pytest:

```bash
$ pytest
```

O podemos ejecutar un archivo de pruebas en específico indicando la ruta:

```bash
$ pytest apps/person/tests.py
```

Si queremos información detallada de las pruebas que se están ejecutando debemos añadir el flag -v al comando:

```bash
$ pytest -v apps/person/tests.py
```

Nota: Si por alguna razón no funciona el pytest, verificar si en la carpeta de apps se encuentra el archivo `__init__.py` y si no existe crearlo, para asegurarse
que Python lo reconozca como un paquete y no se genere ningún error.

Si se requiere probar una gran cantidad de pruebas a la vez, puede suceder que se desee llevar un mejor control visual sobre lo que está sucediendo en cada prueba a tiempo real y con mayor detalle, incluyendo porcentajes. Para esto existe el plugin pytest-sugar que se instala con:

```bash
$ pip install pytest-sugar
```

### Diferencias principales entre unittest y pytest

| Característica | unittest | pytest |
| --- | --- | --- |
| **Sintaxis** | Basada en clases (`TestCase`), más verbosa. | Funciones puras, más Pythonic y limpia. |
| **Aserciones** | Métodos específicos (`self.assertEqual`). | Aserción nativa de Python (`assert`). |
| **Gestión de Datos** | Método `setUp` (se repite en cada test). | Fixtures modulares e inyectables. |
| **Flexibilidad** | Estructura rígida integrada en Django.| Altamente extensible mediante plugins. |
| **Reportes** | Salida estándar de texto / XML. | Permite HTML interactivo y visual (con plugins). |
| **Curva de aprendizaje** | Baja (viene preinstalado). | Media (requiere configuración inicial). |
| **Escalabilidad** | Adecuada para proyectos pequeños. | Excelente para suites de tests complejas. |
| **Documentación** | Buena | Excelente |
| **Ecosistema** | Limitado al core de Django. | +1000 plugins (Sugar, HTML, Coverage). |
| **Veredicto PoC** | Estable y Conservador | Eficiente y Productivo |