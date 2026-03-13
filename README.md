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

$ sudo apt install python3-venv 6X

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

## Validaciones y mensajes de error:

Las validaciones permiten controlar los datos que se ingresan en los formularios y mostrar mensajes de error en caso de que los datos no cumplan con las reglas establecidas, de esta manera se pueden evitar datos incorrectos o no validos que generen errores en la base de datos. Es importante que en un proyecto se apliquen diferentes capas de validación para garantizar la integridad de los datos, así como la correcta retroalimentación al usuario. Estas capas de validación dependen de donde se declaran las validaciones, que pueden ser en el modelo, el formulario o la plantilla como se muestra en los siguientes ejemplos:

### Validaciones en el modelo (Models)

Las validaciones a nivel de base de datos y de la estructura de datos se declaran directamente en los modelos (`models.py`). Se utilizan validadores nativos de Django como `RegexValidator`, `MaxValueValidator` o `MinValueValidator`. Además, en la definición de cada campo se especifica el diccionario `error_messages` para personalizar los mensajes predeterminados y posteriormente mostrarlos en los formularios.

Principalmente importamos los validadores de django o los que deseamos usar:

```python
from django.core.validators import RegexValidator
```

Luego, dentro de la definición de cada campo podemos utilizar estas validaciones de la siguiente manera:

```python
name = models.CharField(
    max_length=100,
    validators=[RegexValidator(r'\d', inverse_match=True, message='No se permiten números.')],
    error_messages={
        'max_length': 'Máximo 100 caracteres.',
        'blank': 'Este campo es requerido.',
        'required': 'Este campo es requerido.',
    }
)
```

En este segmento de código aparte de declarar el campo se definen las validaciones y los mensajes de error que se mostrarán en caso de incumplir con alguna validación.

1. `validators`: Son validadores que se aplican al campo, en este caso se utiliza el `RegexValidator` que valida la expresión regular que se le pasa como parámetro. `r'\d'` valida que no se ingresen números en el campo, `inverse_match=True` invierte la validación, es decir, si la expresión regular no se cumple, se muestra el mensaje de error (`message`).

2. `error_messages`: Es un diccionario que contiene los mensajes de error personalizados que se mostrarán si se ingresa algo que no cumpla con las validaciones que declaramos, como aqui por ejemplo `max_length`.

3. `required`: Es un validador que valida que el campo sea requerido. Cuando envías un formulario y el campo no tiene datos. Django ni siquiera intenta validar el modelo todavía; el formulario lo detiene porque el campo es obligatorio por defecto.

4. `blank`: Es un validador que valida que el campo no sea vacío. Esta es la llave que proteges con tus tests de pytest para que no se permitan campos vacíos. Cuando se llama al método `full_clean()` del modelo, si el modelo tiene un campo sin `blank=True` y se le pasa una cadena vacía (""), se dispara este error. Mientras que 'required' es para formularios web; 'blank' es para el objeto en Python (scripts, consola o tests).

#### Glosario de validaciones en modelos

¬ Para campos de tipo texto como `CharField` y `TextField`:

- `max_length`: Es un validador que valida que el campo no sea mayor a la longitud máxima especificada.

- `min_length`: Es un validador que valida que el campo no sea menor a la longitud mínima especificada.

- `blank`: (Booleano) Si es True, el campo puede quedar vacío en formularios. Si es False, Django obligará a ingresar texto.

- `null`: (Booleano) Afecta a la base de datos. Si es True, Django almacenará los valores vacíos como NULL. (Nota: En textos se prefiere usar blank para evitar estados nulos).

- `choices`: Una lista de tuplas para crear un menú desplegable. Valida que el dato ingresado sea exactamente uno de los permitidos.

- `unique`: (Booleano) Asegura que no existan dos registros con el mismo texto (ej: un código de producto o cédula).

- `db_index`: Crea un índice en la base de datos para acelerar las búsquedas por este campo.

- `prohibit_null_characters`: (Booleano) Evita que se guarden caracteres nulos de bajo nivel (\x00).

¬ Para campos de tipo numérico como `IntegerField`, `DecimalField` y `FloatField`:

- `validators=[MinValueValidator(x)]`: El número no puede ser menor a "x".

- `validators=[MaxValueValidator(x)]`: El número no puede ser mayor a "x".

- `validators=[StepValueValidator(x)]`: El número debe ser múltiplo del valor definido (ej. solo números pares si el paso es 2).

- `max_digits`: (Solo DecimalField) El número total de dígitos permitidos.

- `decimal_places`: (Solo DecimalField) El número de decimales permitidos.

¬ Para campos de tipo fecha como `DateField` y `DateTimeField`:

- `auto_now_add`: Establece la fecha de creación (inmutable después).

- `auto_now`: Actualiza la fecha cada vez que se guarda el registro (auditoría).

- `unique_for_date`: El valor debe ser único para el día especificado.

- `unique_for_month`: El valor debe ser único para el mes especificado.

- `unique_for_year`: El valor debe ser único para el año especificado.

¬ Validadores globales de `django.core.validators` (se aplican a los campos según la necesidad y el tipo):

- `RegexValidator(regex, message=None, code=None)`: Valida que el campo cumpla con la expresión regular especificada.

- `EmailValidator(message=None, code=None)`: Valida que el campo sea un correo electrónico válido.

- `URLValidator(message=None, code=None)`: Valida que el campo sea una URL válida.

- `MinValueValidator(limit_value, message=None, code=None)`: Valida que el campo no sea menor al valor especificado.

- `MaxValueValidator(limit_value, message=None, code=None)`: Valida que el campo no sea mayor al valor especificado.

- `StepValueValidator(limit_value, message=None, code=None)`: Valida que el campo sea múltiplo del valor especificado.

- `validate_slug`: Valida que el texto solo contenga letras, números, guiones o guiones bajos.

- `validate_ipv4_address / validate_ipv6_address`: Valida direcciones IP.

- `validate_comma_separated_integer_list`: Valida una lista de números separados por comas.

- `FileExtensionValidator(allowed_extensions=['extension1', 'extension2'], message="None")`: Valida que un archivo subido tenga una extensión específica (ej. .pdf, .jpg).

Nota: Cualquiera de estos validadores se utilizan añadiendo el parámetro `validators` al campo del modelo. Por ejemplo: `validators=[RegexValidator(r'\d'), validate_slug]`

¬ Restricciones de Nivel Superior (`Meta` class):

Estas validan la relación entre múltiples campos de una sola vez.

- `UniqueConstraint`: Crea una restricción de unicidad compuesta (ej. el par "nombre" y "categoría" no se puede repetir).

- `CheckConstraint`: Permite escribir expresiones lógicas complejas de base de datos (ej. el precio_venta debe ser siempre mayor al precio_costo).

Nota sobre obligatoriedad: En Django, todos los campos son "requeridos" por defecto (`blank=False`). Para permitir que un campo sea opcional, se debe especificar explícitamente `blank=True` (para validación en formularios) y `null=True` (para integridad en la base de datos, excepto en campos de texto). Esto aplica para cualquier tipo de campo.

### Validaciones en el formulario (Forms)

Los formularios (por ejemplo, `ModelForm` en `forms.py`) heredan las validaciones establecidas en los modelos. También es posible definir validaciones adicionales o más complejas a nivel de formulario, ya sea sobreescribiendo el método `clean_<field>()` para reglas específicas de un campo o el método `clean()` de la clase para comprobaciones que relacionen varios datos a la vez. El diccionario `error_messages` también puede definirse sobrescribiendo los campos aquí, o directamente en la clase `Meta`. Esta también es una forma de evitar que se muestren los mensajes de error predeterminados de django y personalizarlos.

En el archivo `forms.py` si quieres validar un solo campo (por ejemplo, que el nombre del producto no contenga la palabra "test"), creas un método con el nombre `clean_` seguido del nombre del campo. Por ejemplo:

```python
class ProductForm(forms.ModelForm):
    # ...
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if "test" in name.lower():
            raise forms.ValidationError("No puedes usar la palabra 'test' en el nombre.")
        return name
```

Si quieres validar varios campos a la vez, creas un método con el nombre `clean()`. Por ejemplo:

```python
class ProductForm(forms.ModelForm):
    # ...
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        if name and price:
            if "test" in name.lower() and price > 100:
                raise forms.ValidationError("No puedes usar la palabra 'test' en el nombre si el precio es mayor a 100.")
        return cleaned_data
```

### Validaciones en la plantilla (Templates)

En los archivos HTML, se puede personalizar el renderizado de los errores. Se itera sobre `form.errors` para capturar todos los problemas e imprimirlos al principio del formulario, dentro de un componente visible de alerta (`<div class="alert alert-danger">`). Como consecuencia, se suprime la visualización nativa de Django bajo la cual los errores de cada `field` se mostrarían de forma separada sobre la caja de entrada.

Por ejemplo para realizar esto en el HTML:

Nos ubicamos donde se encuentran nuestros campos y antes de ellos agregamos el siguiente código:

```html
{% if form.errors %}
    <div class="alert alert-danger" style="color: #721c24; background-color: #f8d7da; border-color: #f5c6cb; padding: 10px; margin-bottom: 20px; border-radius: 5px;">
        <ul style="margin-bottom: 0;">
        {% for field in form %}
            {% for error in field.errors %}
                <li><strong>{{ field.label }}:</strong> {{ error }}</li>
            {% endfor %}
        {% endfor %}
        {% for error in form.non_field_errors %}
            <li>{{ error }}</li>
        {% endfor %}
        </ul>
    </div>
{% endif %}
```

También es posible restringir ingreso de datos erróneos en el template como otra capa de seguridad con el uso de las Validaciones Nativas de
HTML5, por ejemplo: `required`, `min`, `max`, `type`, `pattern`, etc. Por ejemplo:

```html
<input type="text" name="name" required>
<input type="number" name="age" min="0" max="100">
```

Para esto es necesario tener los campos a disposición y no usar el renderizado automático de Django. Pero si queremos añadir estas validaciones y usar el renderizado automático de Django, podemos hacer uso de widgets en el formulario (`forms.py`):

```python
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Nombre del producto',
                'minlength': '5',
                'pattern': '^[a-zA-Z ]+$',
                'title': 'El nombre solo debe contener letras'
            }),
        }
```

#### Glosario de validaciones nativas de HTML5

¬ Validaciones globales (Aplican a casi todos los inputs).

- `required`: Atributo booleano. Si está presente, el usuario no puede enviar el formulario si el campo está vacío.

- `title`: No es una validación como tal, pero si la validación falla, el navegador usa este texto como ayuda en el mensaje flotante (tooltip).

¬ Campos de Texto Corto (`<input type="text">`)

- `minlength`: Define el número mínimo de caracteres permitidos.

- `maxlength`: Define el número máximo de caracteres (el navegador suele bloquear la escritura al llegar al límite).

- `pattern`: El más potente. Recibe una Expresión Regular (Regex). Solo permite enviar el formulario si el texto coincide con el patrón.

    Ejemplo: `pattern="[A-Z]{3}"` (solo permite 3 letras mayúsculas).

¬ Campos Numéricos (`<input type="number">`)

- `min`: El valor numérico mínimo aceptado.

- `max`: El valor numérico máximo aceptado.

- `step`: Define el intervalo legal. Si pones step="10", solo permitirá 10, 20, 30...

¬ Campos de Correo y URL (type="email", type="url")

- Validación de Formato Nativa: El navegador verifica automáticamente que el texto tenga una estructura válida (ej. que contenga un @ y un dominio en el caso del email).

¬ Areas de Texto Largo (`<textarea>`)

- `minlength / maxlength`: Al igual que en el texto corto, controlan la extensión del contenido.

Nota: Las áreas de texto no soportan el atributo pattern.

### Validaciones en las vistas (Views):

Se pueden agregar validaciones en las vistas como otra capa de restricción donde limitaremos la continuidad del flujo de ejecución si no se cumplen ciertas condiciones, donde podemos validar antes, durante o después de procesar el formulario. Por ejemplo:

Dentro de la clase `ProductCreateView` declaramos la función que utilizaremos para validar antes de procesar el formulario:

```python
class ProductCreateView(CreateView):
    # ...
    def dispatch(self, request, *args, **kwargs):
        # Validación a nivel de vista
        if Product.objects.count() >= 100:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied("Límite de productos alcanzado.")
        return super().dispatch(request, *args, **kwargs)
```

También se pueden sobreescribir los métodos `form_valid()` y `form_invalid()`:

```python
class ProductCreateView(CreateView):
    # ...
    def form_valid(self, form):
        # Validar antes de procesar el formulario
        if form.is_valid():
            # Procesar el formulario
            form.save()
            return super().form_valid(form)
```

### Mensajes de error automáticos según el idioma

Django cuenta con un sistema integrado de traducciones (i18n). Si los `error_messages` no se definen manualmente ("This field is required", etc), Django arrojará sus mensajes de validaciones predeterminados. Si en `settings.py` la variable `LANGUAGE_CODE` está configurada para un localismo distinto (como `'es'` para español) y los middlewares de Locale están habilitados, Django traducirá estos componentes al español u otro idioma automáticamente.

Si deseamos cambiar el idioma por defecto, debemos cambiar la variable `LANGUAGE_CODE` en `settings.py`:

```python
LANGUAGE_CODE = 'es'
```

### Restricciones a nivel de base de datos (Constraints)

Adicional a las validaciones de las formas o modelos normales, Django permite incluir en la clase `Meta` de los modelos configuraciones directas a las tablas de la base de datos SQL, mediantes la directiva `constraints` (ej. `models.UniqueConstraint` o `models.CheckConstraint`). Estas configuran reglas a nivel de SQL garantizando que los registros de la capa física de la base nunca violen la regla de negocio al forzar este chequeo desde el propio motor de la base de datos.

Si deseamos agregar una restricción de unicidad a un campo, por ejemplo, el email, debemos agregar la siguiente línea en la clase `Meta` del modelo:

```python
class Meta:
    constraints = [
        models.UniqueConstraint(
            fields=['email'],
            name='unique_email',
            condition=models.Q(is_active=True),
        ),
    ]
```

Nota: Los constraints son una capa adicional de seguridad que si bien no reemplazan las validaciones de las formas o modelos normales, sí pueden ser útiles para garantizar que los registros no violen alguna regla de negocio al forzar este chequeo desde el propio motor de la base de datos.

#### Glosario de constraints

- `CheckConstraint`

Es una regla lógica que permite validar una condición específica (una expresión booleana) directamente en el motor de la base de datos. Sirve para asegurar que los valores de uno o varios campos cumplan con una lógica aritmética o comparativa antes de ser guardados.

Ejemplo: Asegurar que el precio de un producto siempre sea mayor a cero.

```python
models.CheckConstraint(check=models.Q(price__gt=0), name='price_positive_check')
```

- `UniqueConstraint`

Es una restricción que garantiza que el valor de un campo, o la combinación de varios campos, no se repita en ninguna otra fila de la tabla. Sirve para prevenir la duplicidad de datos críticos que deben ser únicos por identidad o por regla de negocio.

Ejemplo: Evitar que existan dos productos con el mismo nombre exacto.

```python
models.UniqueConstraint(fields=['name'], name='unique_product_name')
```

- `UniqueConstraint` (Compuesto)

Es una variante que se aplica sobre un conjunto de campos. Sirve para permitir que un valor se repita en un campo, siempre y cuando la combinación con el segundo campo sea distinta.

Ejemplo: Un producto puede tener el mismo nombre que otro, siempre que pertenezcan a categorías diferentes.

```python
models.UniqueConstraint(fields=['name', 'category'], name='unique_name_per_category')
```

- `ForeignKey` Constraint (Integridad Referencial)

Es una restricción que vincula una columna de una tabla con la clave primaria de otra. Sirve para garantizar que no existan registros huérfanos; es decir, no puedes asociar un producto a una categoría que no existe en la base de datos.

Ejemplo: Si se elimina una categoría, decidir si se borran sus productos o si se impide la eliminación.

```python
category = models.ForeignKey(Category, on_delete=models.CASCADE)
```

- `primary_key` Constraint

Es la restricción fundamental que identifica de forma unívoca cada registro en una tabla. Sirve para que el motor de la base de datos pueda indexar, buscar y relacionar cada fila de manera eficiente y sin ambigüedades. No permite valores nulos ni duplicados.

Ejemplo: El campo id que Django crea automáticamente.

```python
id = models.AutoField(primary_key=True)
```

### Desactivación de validaciones del navegador (`novalidate`)

A las etiquetas `<form>` en los templates HTML se les puede añadir el atributo opcional `novalidate` (`<form method="post" novalidate>`). Esto desactiva todas las validaciones nativas visuales del navegador al momento de pulsar Submit (como los pequeños tooltip que varían por explorador web previniendo formularios vacíos, etc). Al incluirlo, recibimos los datos del formulario directamente sin filtros a Django y delegamos todo el trabajo de control, la validación y el renderizado estético de errores a nuestro Backend.

Si en algún momento se presenta el momento donde se muestra un mensaje que no reconoces haber creado o una validación que no se ha implementado, es posible que el explorador web esté intentando aplicar validaciones por defecto. En este caso, puedes desactivarlas agregando el atributo `novalidate` a la etiqueta `<form>`.

Sin embargo, en algunos proyectos la validación del navegador puede funcionar como otra capa de seguridad, por lo que en algunos casos es preferible mantenerla activada.