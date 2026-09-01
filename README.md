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

## Creating an admin user

First we’ll need to create a user who can login to the admin site. Run the
following command:

```bash
$ python manage.py createsuperuser
```

Enter your desired username and press enter.

Username: admin

You will then be prompted for your desired email address:

Email address: admin@example.com

The final step is to enter your password. You will be asked to enter your
password twice, the second time as a confirmation of the first.

Password: #####
Password (again): *********
Superuser created successfully.

## Image

![1.png](1.png "1.png")

![2.png](2.png "2.png")

![3.png](3.png "3.png")

![4.png](4.png "4.png")

===========================================================================
Usuarios, Grupos/Roles, Permisos en Django (Funciones nativas sin paquetes)
===========================================================================

En Django (incluyendo Django 6), el sistema de autenticación viene integrado de
forma nativa a través de django.contrib.auth.

No existe el concepto de "Rol" como una entidad explícita en el código de
Django: los "Roles" en Django son los Grupos (Group), y la estructura de control
de acceso se basa en la combinación de Usuarios, Grupos y Permisos.

1. ¿Cómo funcionan las piezas?

El modelo de autorización nativo de Django se compone de tres elementos
interconectados:

-Permisos (Permission): Representan la acción específica que se puede o no
realizar sobre un modelo (crear, leer, actualizar, borrar).

-Grupos (Group): Funcionan como los Roles. Son etiquetas que agrupan a un
conjunto de permisos y se le puden asignar a los usuarios.

-Usuarios (User): Pueden tener permisos asignados directamente o heredar los
permisos de los Grupos a los que pertenecen.

[Usuario] -> Pertenece a -> [Grupo] -> Tiene asignados -> [Permisos]
    |                                                          ^
    +--------------------- O asignados directamente -----------+

2. Los Permisos por Defecto

Cada vez que creas y migras un modelo en Django, el framework genera
automáticamente 4 permisos predeterminados por cada modelo:

1. add_<nombre_modelo> (Crear)
2. change_<nombre_modelo> (Editar)
3. delete_<nombre_modelo> (Eliminar)
4. view_<nombre_modelo> (Ver/Consultar)

3. Verificar Permisos en el Código

Django evalúa automáticamente los permisos del usuario sumando sus permisos
individuales + los permisos de todos los grupos a los que pertenece.

El formato del nombre del permiso siempre es: app_label.codename.

En Vistas Basadas en Funciones (FBV) se usa el decorador @permission_required:

-----

from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
from .forms import PersonForm
from django.contrib.auth.decorators import permission_required


@permission_required('person.add_person', raise_exception=True)
def create_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person:home')
    else:
        form = PersonForm()

    context = {'form': form}
    return render(request, 'person/create.html', context)


@permission_required('person.delete_person', raise_exception=True)
def delete_person(request, pk):
    person = get_object_or_404(Person, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person:home')

    context = {'person': person}
    return render(request, 'person/delete.html', context)

-----

En Vistas Basadas en Clases (CBV) se usa el mixin PermissionRequiredMixin:

-----

from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Display the form and create a product"""
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product:home')

    # Permiso requerido
    permission_required = 'product.add_product'

    # Lanza 403 HTTP Forbidden si no tiene el permiso
    raise_exception = True


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    """Confirm and delete a product"""
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('product:home')

    # Permiso requerido
    permission_required = 'product.delete_product'

    # Lanza 403 HTTP Forbidden si no tiene el permiso
    raise_exception = True

-----

Validación práctica de la teoría con ejemplos reales
===================================================

1. Clona el repositorio: https://github.com/argenisosorio/Django_6_crud/

2. Cambia a la rama: test/users-groups-permissions

3. Ejecuta las migraciones para crear la base de datos y genera un usuario
administrador (superuser) desde la terminal.

4. Inicia sesión en el panel de administración de Django
(http://127.0.0.1:8000/admin/) con la cuenta del administrador. Si luego visitas
http://127.0.0.1:8000/, verás el mensaje de bienvenida con el usuario
autenticado.

5. En el panel de administración, ve a la sección "Authentication and
Authorization" > "Groups" y crea los siguientes grupos:

a) Grupo "CRUD Person": Asigna los siguientes permisos (trasládalos de la
columna izquierda a la derecha):

- Person | person | Can add person
- Person | person | Can change person
- Person | person | Can delete person
- Person | person | Can view person

Esto otorga control total sobre el modelo Person a los miembros de este grupo.
Haz clic en "Guardar".

b) Grupo "CRUD Product": Asigna los siguientes permisos:

- Product | product | Can add product
- Product | product | Can change product
- Product | product | Can delete product
- Product | product | Can view product

Esto otorga control total sobre el modelo Product a los miembros de este grupo.
Haz clic en "Guardar".

6. Crea dos usuarios regulares en la sección "Users" del panel de
administración:

- Usuario: test
* Marca la casilla "is_staff" en True (para permitir el acceso al panel).
* En la sección "Groups", asigna el grupo "CRUD Person".

- Usuario: test2
* Marca la casilla "is_staff" en True.
* En la sección "Groups", asigna el grupo "CRUD Product".

Resumen de usuarios creados:

Usuario  | Grupo
---------+--------------
test     | CRUD Person
test2    | CRUD Product

7. Cierra la sesión del administrador e inicia sesión con el usuario "test".
Navega a http://127.0.0.1:8000/ para verificar el saludo de bienvenida.

A continuación, prueba la gestión de permisos:

-Interactúa con el modelo Person en el CRUD: el sistema te permitirá realizar todas las
operaciones.

-Intenta interactuar con el modelo Product: el sistema responderá con un error
HTTP 403 Forbidden, ya que el usuario no posee los permisos requeridos.

Cierra la sesión del usuario test e inicia sesión con el usuario "test2".
Navega a http://127.0.0.1:8000/ para verificar el saludo de bienvenida.

A continuación, prueba la gestión de permisos:

-Interactúa con el modelo Person en el CRUD: El sistema responderá con un error
HTTP 403 Forbidden, ya que el usuario no posee los permisos requeridos.

-Intenta interactuar con el modelo Product: El sistema te permitirá realizar
todas las operaciones.

Fuente
======

Gemini IA

Permisos Personalizados (Custom Permissions)
============================================

Si los 4 permisos por defecto no son suficientes, puedes definir permisos
propios dentro de la clase Meta de tu modelo:

-----

from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    age = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = [
            ("list_persons", "Can list persons"),
        ]

-----

Crear una nueva migración y aplicar la nueva migración:

$ python manage.py makemigrations person

Migrations for 'person':
  apps/person/migrations/0002_alter_person_options.py
    ~ Change Meta options on person

$ python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, person, product, sessions
Running migrations:
  Applying person.0002_alter_person_options... OK

Lo anterior quiere decir que se creó el nuevo permiso para el modelo Persona.

Si intentamos craer un nuevo grupo o editamos alguno de los grupos veremos
el nuevo permiso "Can list persons".

from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
from .forms import PersonForm
from django.contrib.auth.decorators import permission_required


@permission_required('person.list_persons', raise_exception=True)
def home(request):
    """
    Display the home page listing all Person records.

    Args:
        request (HttpRequest): The incoming HTTP request

    Returns:
        HttpResponse: Rendered template with all Person objects
    """
    people = Person.objects.all()
    context = {
        'people': people,
        'message': '¡Hello Django 6 Person CRUD!',
    }
    return render(request, 'person/home.html', context)

y en el caso de Product con CBV:

-----

from django.db import models


class Product(models.Model):
    """
    Represents a product in the system.
    """

    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        String representation of the Product model.

        Returns:
            str: The product's name for easy identification in admin and queries.
        """
        return self.name

    class Meta:
        permissions = [
            ("list_products", "Can list products"),
        ]

-----

class ProductListView(PermissionRequiredMixin, ListView):
    """Displays the product list"""
    model = Product
    template_name = 'product/home.html'
    context_object_name = 'products'

    # Permiso requerido
    permission_required = 'product.list_products'

    # Lanza 403 HTTP Forbidden si no tiene el permiso
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = '¡Hello Django 6 Product CRUD!'
        return context

-----

Verificación Manual en código Python: Puedes usar el método has_perm() en
cualquier objeto usuario:

-----

if request.user.has_perm('person.list_persons'):
    print("----- User has the 'person.list_persons' permission. -----")
else:
    print("----- User does NOT have the 'person.list_persons' permission. -----")

-----

En Plantillas (Templates):

Django pasa automáticamente la variable perms al contexto de la plantilla:

-----

{% if perms.mi_app.can_publish %}
    <a href="{% url 'publicar' articulo.id %}">Publicar Artículo</a>
{% endif %}

Ejemplo real:

{% if perms.person.list_persons %}
    Has permission to list persons.
{% else %}
    Does NOT have permission to list persons.
{% endif %}

-----

Resumen
=======

¿Hay Permisos? Sí, nativos. Se crean 4 automáticamente por cada modelo (add,
change, delete, view) y puedes crear los tuyos en la clase Meta.

¿Qué son los grupos? Son agrupaciones de permisos.

¿Cómo interactúan? Los Permisos se asignan a los Grupos, y los Usuarios se
añaden a los Grupos para heredar esos permisos de forma limpia y escalable.

Fuente
======

Gemini IA
