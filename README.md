# Django 6 CRUD Example + Bootstrap 5

El siguiente es un ejemplo de CRUD (Crear, Leer, Actualizar, Eliminar) en
Django 6.

## Patrón de Arquitectura

Este proyecto se desvía del patrón estándar de Django MVT. En su lugar,
implementa una Arquitectura en Capas.

Este enfoque desacopla la lógica empresarial central del marco HTTP (Django), lo
que hace que la aplicación sea significativamente más fácil de probar, mantener
y escalar a medida que crece.

## Las capas

### Controladores ( controllers/):

- Actúa como punto de entrada para solicitudes HTTP (reemplazando las vistas
tradicionales de Django). Responsable únicamente de manejar solicitudes HTTP,
validar la entrada, llamar al Servicio apropiado y devolver una respuesta HTTP
(representando una plantilla o redirigiendo).

- No contienen ninguna lógica empresarial.

### Solicitudes ( requests/):

- Manejar la validación de datos HTTP entrantes (por ejemplo, datos POST).

- Generalmente se implementa mediante formularios Django para garantizar que los
datos estén limpios y válidos antes de que lleguen a la capa de lógica
empresarial.

### DTO - Objetos de transferencia de datos ( dtos/):

- Estructuras de datos simples (a menudo Python) dataclasses o clases estándar
que se utilizan para pasar datos entre la capa del controlador y la capa de
servicio.

- Se aseguran de que la capa de Servicio no dependa de objetos específicos de
HTTP como request.POST o formularios Django.

### Servicios ( services/):

- El corazón de la aplicación. Esta capa contiene toda la lógica de negocio y
los casos de uso.

- Los servicios toman DTO como entrada, realizan las operaciones necesarias (como
crear un empleado, enviar correos electrónicos, calcular salarios) e interactúan
con la base de datos a través de modelos o selectores.

### Selectores ( selectors/):

- Dedicado a consultas de bases de datos complejas y obtención de datos
(operaciones de lectura).

- Si bien las consultas simples pueden residir en los Servicios, los Selectores
mantienen limpia la capa de Servicio abstrayendo búsquedas ORM complejas.

### Modelos ( models/):

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
├── apps                              # Directorio de aplicaciones
│   ├── persons                       # Aplicación principal
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── controllers               # Controladores de solicitudes HTTP (Vistas)
│   │   │   ├── person_controller.py
│   │   ├── dtos                      # Objetos de transferencia de datos
│   │   │   ├── person_dto.py
│   │   ├── models                    # Esquemas de base de datos (Django ORM)
│   │   │   ├── person.py
│   │   ├── requests                  # Validación de entrada (Formularios)
│   │   │   ├── create_person.py
│   │   │   └── update_person.py
│   │   ├── selectors                 # Operaciones de lectura de base de datos
│   │   ├── services                  # Lógica empresarial central (operaciones de escritura)
│   │   │   ├── person_service.py
│   │   ├── templates                 # Plantillas HTML para la interfaz de usuario
│   │   │   ├── persons
│   │   │   │   ├── create_person.html
│   │   │   │   ├── index.html
│   │   │   │   └── update.html
│   │   └── urls.py
```

## Flujo de la apliación

### Index

1- Al entrar al proyecto se carga la url "" que apunta a la aplicación Persons,
esta url apunta al método index definido en controllers.person_controller el
cuál es una vista para mostrar la lista de personas, esta vista recupera todas
las personas utilizando el servicio get_all_persons de services/person_service
y las pasa al template para su renderizado. El servicio get_all_persons se
encarga de hacer la consulta de todas las personas usando el modelo Person
declarado en models/person.py.

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
