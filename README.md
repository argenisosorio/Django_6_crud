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

## Para ejecutar la tarea en segundo plano para envío de mail:
- Instalar los paquetes django_tasks y django_tasks_db (ya agregados en requirements.txt) dentro del entorno virtual

- Ejecutar python manage.py, en la que se han agregado automáticamente comandos para django_tasks_db

    [django_tasks_db]
    db_worker
    prune_db_task_results

- Ejecutar migraciones

- Agregar los datos del smtp en el settings.py

- Ejecutar el worker 

```bash
$ python manage.py db_worker

$ pip install django_tasks django_tasks_db

$ python manage.py migrate

$ vim Django_6_crud/settings.py

$ python manage.py db_worker
```

## Test the project:

Open your browser to http://127.0.0.1:8000 and you'll see the Django 6 CRUD
application for managing people records.

## Image

![1.png](1.png "1.png")

![2.png](2.png "2.png")

![3.png](3.png "3.png")

![4.png](4.png "4.png")
