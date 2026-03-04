# Django 6 CRUD - Arquitectura en Capas

El siguiente es un ejemplo de CRUD (Crear, Leer, Actualizar, Eliminar) en
Django 6 bajo una Arquitectura en Capas.

Basado en el proyecto
[https://github.com/NatanaelRojo/django-service-demo](https://github.com/NatanaelRojo/django-service-demo)
de Natanael.

## Patrón de Arquitectura

Este proyecto se desvía del patrón estándar de Django MVT. En su lugar,
implementa una Arquitectura en Capas.

Este enfoque desacopla la lógica empresarial central del marco HTTP (Django), lo
que hace que la aplicación sea significativamente más fácil de probar, mantener
y escalar a medida que crece.

## Las capas

### Controladores (controllers/):

- Actúa como punto de entrada para solicitudes HTTP (reemplazando las vistas
tradicionales de Django). Responsable únicamente de manejar solicitudes HTTP,
validar la entrada, llamar al Servicio apropiado y devolver una respuesta HTTP
ya sea devolviendo mensajes, una plantilla html o redirigiendo.

- No contienen ninguna lógica empresarial.

### Solicitudes (requests/):

- Maneja la validación de datos HTTP entrantes (por ejemplo, datos POST).

- Se implementa mediante formularios Django para garantizar que los datos estén
limpios y válidos antes de que lleguen a la capa de lógica empresarial.

### DTO - Objetos de transferencia de datos (dtos/):

- Estructuras de datos simples (a menudo Python) dataclasses o clases estándar
que se utilizan para pasar datos entre la capa del controlador y la capa de
servicio.

- Se asegura de que la capa de Servicio no dependa de objetos específicos de
HTTP como request.POST o formularios Django.

### Servicios (services/):

- Esta capa contiene toda la lógica de negocio y los casos de uso.

- Los servicios toman DTO como entrada, realizan las operaciones necesarias
(como crear un registro en la BD, enviar correos electrónicos, calcular
salarios) e interactúan con la base de datos a través de modelos o selectores.

### Selectores (selectors/):

- Dedicado a consultas de bases de datos complejas y obtención de datos
(operaciones de lectura).

- Si bien las consultas simples pueden residir en los Servicios, los Selectores
mantienen limpia la capa de Servicio abstrayendo búsquedas ORM complejas.

### Modelos (models/):

- Modelos ORM estándar de Django.

- Representan las tablas y relaciones de la base de datos, pero se mantienen
"simples" (desprovistas de lógica empresarial compleja).

## ¿Por qué este patrón?

- Separación de preocupaciones: la lógica HTTP está separada de la lógica
empresarial.

- Capacidad de prueba: puede probar servicios y DTO de forma aislada sin
necesidad de una solicitud HTTP simulada o un servidor web.

- Reutilización: la lógica de negocios en los servicios se puede llamar desde
cualquier lugar (controladores, tareas de Celery, comandos de administración,
API) sin duplicar código.

## Estructura del proyecto

```
├── Django_6_crud                     # Configuración del proyecto Django (configuraciones, URL raíz)
│   ├── settings.py
│   ├── urls.py
├── manage.py
├── README.md
├── requirements.txt
├── static                            # Archivos estátidos del proeycto como hojas de estilos, imágenes, entre otros.
├── apps                              # Directorio de aplicaciones.
│   ├── persons                       # Aplicación principal.
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── controllers               # Controladores de solicitudes HTTP (Vistas).
│   │   │   ├── person_controller.py
│   │   ├── dtos                      # Objetos de transferencia de datos.
│   │   │   ├── person_dto.py
│   │   ├── models                    # Esquemas de base de datos (Django ORM).
│   │   │   ├── person.py
│   │   ├── requests                  # Validación de entrada (Formularios).
│   │   │   ├── create_person.py
│   │   │   └── update_person.py
│   │   ├── selectors                 # Operaciones de lectura de base de datos.
│   │   ├── services                  # Lógica empresarial central (operaciones de escritura).
│   │   │   ├── person_service.py
│   │   ├── templates                 # Plantillas HTML para la interfaz de usuario.
│   │   │   ├── persons
│   │   │   │   ├── create_person.html
│   │   │   │   ├── index.html
│   │   │   │   └── update.html
│   │   └── urls.py
```

## Flujo de la apliación

### Index

Al ingresar a la raíz del proyecto (/), la URL redirige a la aplicación Persons,
invocando el método index definido en controllers.person_controller. Esta vista
se encarga de listar todas las personas registradas en el sistema. Para ello,
utiliza el servicio get_all_persons de services/person_service, el cual consulta
la base de datos a través del modelo Person declarado en models/person.py. Los
resultados se pasan al template correspondiente para su renderización.

### Create

Desde la página principal, al hacer clic en "Add New Person", se accede a la
URL /create/, que activa el método create definido en
controllers.person_controller. Esta vista muestra el formulario de registro de
nuevas personas. Al enviar el formulario mediante el botón "Submit", los datos
se envían vía POST al método store.

### Store

El método store (ubicado en controllers.person_controller) procesa la creación
de una nueva persona. Valida los datos recibidos utilizando CreatePersonRequest,
un formulario importado de requests.create_person que incluye validaciones
y mensajes de error personalizados.

- Si los datos no son válidos, se retorna un error HTTP 400 con los mensajes de
validación.

Si son válidos, se encapsulan en un DTO (Data Transfer Object) llamado PersonDTO
que permite transferir datos de manera estructurada entre capas, desacoplando la
lógica de negocio de la presentación.

Posteriormente, se invoca al servicio create_person de services.person_service,
que persiste la nueva persona en la base de datos y retorna la instancia creada.
Finalmente, store redirige al listado de personas.

### Edit

Desde el listado principal, al hacer clic en "Edit" sobre una persona específica
se accede a la URL /edit/<id>/, que activa el método edit del controlador. Esta
vista recupera los datos de la persona mediante el servicio get_person y los
muestra en un formulario pre-cargado para su edición. Al hacer clic en
"Update Person", los datos modificados se envían vía POST al método update.

### Update

El método update (también en controllers.person_controller) gestiona la
actualización de una persona existente. Recibe el ID de la persona y los datos
del formulario, los cuales son validados mediante UpdatePersonRequest (definido
en requests.update_person), que aplica reglas de validación específicas y
mensajes de error personalizados.

- Si la validación falla, se retorna un error con los detalles.

 Si es exitosa, los datos se encapsulan en un UpdatePersonDTO y se pasan al
 servicio update_person de services.person_service, que actualiza la información
 en la base de datos.

Una vez completada la operación, se redirige al listado de personas.

### Delete

Desde la página principal, al hacer clic en "Delete" sobre una persona, se envía
una solicitud POST a la URL /delete/<id>/, que ejecuta el método delete del
controlador. Esta vista recibe el ID de la persona a eliminar y utiliza el
servicio delete_person para remover el registro del sistema. Tras la
eliminación, redirige automáticamente al listado de personas.

## Requirimientos
```
Django==6.0.2
Python>=3.12
```

## Instalación de requerimientos

```bash
$ pip install -r requirements.txt

$ cp Django_6_crud/settings.py_example Django_6_crud/settings.py

$ python manage.py makemigrations persons product

$ python manage.py migrate

$ python manage.py runserver
```

## Prueba el proyecto

Abra su navegador en http://127.0.0.1:8000 y verá la aplicación CRUD de Django 6
para administrar registros de personas.

## Imagen

![1.png](1.png "1.png")
