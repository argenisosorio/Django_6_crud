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

## Declarar relaciones entre modelos (Comparación entre Django y Laravel)

Mientras que en Laravel se declaran las relaciones en el modelo con el siguiente formato:

```php
// Se declara la relación en el modelo de Personas
public function product()
{
    return $this->belongsTo(Product::class);
}

// Se declara la llave foránea aparte en la migración
$table->foreignId('product_id')
        ->nullable()
        ->constrained('products')
        ->nullOnDelete();

// Se declara la relación en el modelo de Productos
public function people()
{
    return $this->hasMany(Person::class);
}
```

En Django se declara tanto la llave foránea como las relaciones en el modelo con el siguiente formato:

```python
# Se declara la llave foránea y la relación en el modelo de Personas
product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name='people')
```
La principal diferencia radica en que los modelos en Django son más completos y versátiles que en Laravel, no dependen de migraciones aparte para crear relaciones entre modelos, ya que se declaran en el mismo modelo; lo que facilita el desarrollo y mantenimiento de las aplicaciones.

Otra diferencia es que en Laravel se utilizan métodos como `belongsTo`, `hasMany`, `hasOne`, `belongsToMany` para declarar el tipo de relación, mientras que en Django se utilizan tipos de campo como `ForeignKey`, `OneToOneField`, `ManyToManyField`.

Lo interesante aquí es que para poder relacionar de manera simétrica una relación de 1:N | N:1, no es necesario declarar una relación inversa de manera explícita, basta con declararla en uno de ellos y que especifiques el parámetro `related_name`.

¿Por qué sucede esto? Así como Laravel funciona con un método llamado getRelationType(), Django obtiene la relación inversa gracias a los flags que tienen asignados cada tipo de campo.

Cuando por ejemplo definimos el related_name='people', Django crea un objeto virtual en el modelo Product. Ese objeto virtual tendrá el flag one_to_many = True. Así es como Django sabe que product.people.all() debe devolver una lista y no un solo objeto.