```
========================================
Probando Docker en un proyecto de Django
========================================

Este manual fue probado en en Debian 13.

1. Revisar los requerimientos y configuraciones del SO y la máquina en la
sección anterior > https://github.com/argenisosorio/docker_python_hello_world

2. Instalar Docker Engine descrito en la sección anteior.

3. Verificar que la instalación sea exitosa corriendo la imagen hello-world
descrito en la sección anteior.

En este ejemplo vamos a ejecutar un proyecto de Django con una base de datos
de Postgresql.

Estructura de archivos necesaria para la prueba:

mi_proyecto_django/
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── start.sh
├── .env
├── requirements.txt
├── manage.py
└── ...

¿Dónde crear cada archivo?
==========================

+----------------------+------------------------+-----------------------+
| Archivo              | Ubicación              | ¿Crearlo manualmente? |
+----------------------+------------------------+-----------------------+
| Dockerfile           | Raíz del proyecto      | Sí                    |
+----------------------+------------------------+-----------------------+
| docker-compose.yml   | Raíz del proyecto      | Sí                    |
+----------------------+------------------------+-----------------------+
| Makefile             | Raíz del proyecto      | Sí                    |
+----------------------+------------------------+-----------------------+
| start.sh             | Raíz del proyecto      | Sí                    |
+----------------------+------------------------+-----------------------+
| .env                 | Raíz del proyecto      | Sí                    |
+----------------------+------------------------+-----------------------+
| requirements.txt     | Raíz del proyecto      | Sí (si no existe)     |
+----------------------+------------------------+-----------------------+

Dockerfile
==========

#1. Define la imagen base: Usamos una versión ligera (slim) de Python 3.12.

FROM python:3.12-slim

#2. Crea y se mueve a la carpeta /app dentro del contenedor para organizar los
#archivos. /app no es una aplicación específica, es simplemente una carpeta
#(directorio) dentro del contenedor. El comando indica que cree una carpeta
#llamada 'app' en la raíz del sistema operativo del contenedor y, a partir de
#ahora, ejecute todos los comandos ahí dentro".

WORKDIR /app

#3. Copia solo el archivo de dependencias. Se hace antes para que Docker no
#reinstale todo cada vez que cambies una línea de código (aprovecha la memoria
#caché).

COPY requirements.txt .

#4. Instala las librerías de Python listadas en el archivo, sin guardar archivos
#temporales.

RUN pip install --no-cache-dir -r requirements.txt

#5. Copia todo el contenido de tu proyecto actual al directorio de trabajo del
#contenedor.

COPY . .

#6. Cambia los permisos del archivo start.sh para asegurar que el sistema pueda
#ejecutarlo.

RUN chmod +x start.sh

#7. Indica que el contenedor escuchará peticiones en el puerto 8000 (estándar de
#Django).

EXPOSE 8000

#8. Define el comando final que arranca la aplicación al iniciar el contenedor.

CMD ["./start.sh"]

-----

¿Cómo funciona este proceso?

Para visualizarlo mejor, imagina que un Dockerfile es una receta de cocina que
construye una computadora miniatura aislada:

Capas (Layers): Cada instrucción (FROM, COPY, RUN) crea una capa. Si no cambias
el requirements.txt, Docker es inteligente y salta el paso de instalación,
haciendo que todo sea más rápido.

Aislamiento: Todo lo que instalas ahí dentro no afecta a tu computadora
personal; vive solo dentro de esa "caja" (contenedor).

docker-compose.yml
==================

services:
  db:
    image: postgres:15
    container_name: django_postgres
    restart: always
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5

  web:
    build: .
    container_name: django_app
    restart: always
    ports:
      - "8000:8000"
    volumes:
      - .:/app
    depends_on:
      db:
        condition: service_healthy
    env_file:
      - .env
    command: ["./start.sh"]

volumes:
  postgres_data:

-----

Si el Dockerfile era la receta para crear un solo componente, el archivo
docker-compose.yml es el director de orquesta. Su trabajo es hacer que varios
contenedores (en este caso, tu base de datos y tu app de Django) trabajen
juntos sin que tengas que configurarlos uno por uno.

Cada bloque que ves debajo de la palabra services: representa un contenedor
independiente.

1. El Servicio db (La Base de Datos)

Este bloque levanta una base de datos PostgreSQL.

-image: postgres:17: No necesita un Dockerfile propio; descarga la imagen
oficial de Postgres versión 17.

-environment: Aquí usa variables (como ${DB_NAME}). Docker las busca en un
archivo llamado .env para no escribir las contraseñas reales directamente en el
código.

-volumes (postgres_data): Esto es vital. Los contenedores son volátiles (si se
borran, se pierde todo). El volumen asegura que tus datos se guarden en tu
disco duro real y no se borren al apagar Docker.

healthcheck: Es un "examen médico". Django no intentará conectarse hasta que
Postgres diga: "¡Estoy listo para recibir datos!".

2. El Servicio web (Tu App Django)

Este bloque es el que usa el Dockerfile que vimos antes.

-build: .: Le dice a Docker: "Busca el Dockerfile en esta misma carpeta y
construye la imagen".

-ports: "8000:8000": Conecta el puerto 8000 de tu computadora con el 8000 del
contenedor. Por eso puedes entrar a localhost:8000 en tu navegador.

-volumes: .:/app: ¡Ojo aquí! Esto es para desarrollo. Significa que cualquier
cambio que hagas en tu código en VS Code se reflejará instantáneamente dentro
del contenedor sin tener que reconstruirlo.

-depends_on: Le dice a la app: "No arranques hasta que la base de datos esté
saludable (service_healthy)". Esto evita el típico error de Django intentando
conectar a una base de datos que aún se está encendiendo.

-env_file: .env: Carga todas tus configuraciones secretas (SECRET_KEY, DB_USER,
etc.) desde el archivo .env.

En resumen: ¿Qué pasa cuando haces docker-compose up?

-Crea una red interna para que web y db puedan hablar entre ellos usando sus
nombres (Django usará el host db en lugar de una IP).

-Enciende Postgres y espera a que pase el "healthcheck".

-Construye tu app Django usando el Dockerfile.

-Conecta los cables: Mapea los puertos y monta los volúmenes para que tu código
y tus datos estén seguros.

-Nota importante: Asegúrate de tener un archivo llamado .env en la misma carpeta
con las variables DB_NAME, DB_USER y DB_PASSWORD, de lo contrario, el servicio
db fallará.

¿Por qué se usan 2 y no metemos todo en uno solo?

Aunque podrías meter todo en un solo contenedor, la filosofía de Docker es "un
proceso por contenedor". Esto tiene varias ventajas:

-Independencia: Si quieres actualizar la versión de la base de datos (por
ejemplo, pasar de Postgres 17 a 18), puedes hacerlo sin tocar el contenedor de
Django.

-Seguridad: El contenedor web es el único que da la cara al internet (puerto
8000). El contenedor db vive en una red interna y solo habla con web.

-Recursos: Si tu app crece mucho, podrías decirle a Docker que use más memoria
para la base de datos y menos para la web, de forma separada.

settings.py
===========

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': 'db',
        'PORT': '5432',
    }
}

-----

Le decimos a la Django que las variables para conectarse a la base de datos las
va a leer en el .env

start.sh
========

#!/bin/bash

echo "----- Esperando a que PostgreSQL esté listo..."
sleep 5

echo "----- ¡PostgreSQL está listo! Procediendo con las tareas de Django..."

# Ejecutando migraciones
# --no-input evita que el script se detenga pidiendo confirmaciones
echo "----- Revisando cambios en los modelos..."
python manage.py makemigrations person product --no-input

echo "----- Aplicando migraciones a la base de datos..."
python manage.py migrate --no-input

# Iniciando el servidor de desarrollo
echo "----- Iniciando servidor Django en http://0.0.0.0:8000"
python manage.py runserver 0.0.0.0:8000

Makefile
========

# Variable que define el archivo de configuración de Docker Compose a utilizar
DEV_COMPOSE_FILE := docker-compose.yml

# Construir la imagen
build:
	# Ejecuta la construcción de las imágenes definidas en el archivo compose
	docker compose -f $(DEV_COMPOSE_FILE) build

# Levantar los contenedores
up:
	# Crea e inicia los contenedores (bloquea la terminal para ver la salida)
	docker compose -f $(DEV_COMPOSE_FILE) up

# Levantar en segundo plano
up-d:
	# Inicia los contenedores en modo "detached" (corriendo en el fondo)
	docker compose -f $(DEV_COMPOSE_FILE) up -d

# Detener contenedores
down:
	# Detiene y elimina los contenedores y redes creadas por el compose
	docker compose -f $(DEV_COMPOSE_FILE) down

# Ver logs
logs:
	# Muestra y sigue en tiempo real las salidas/errores de los contenedores
	docker compose -f $(DEV_COMPOSE_FILE) logs -f

# Ejecutar comandos dentro del contenedor
shell:
	# Abre una terminal interactiva (bash) dentro del contenedor de Django
	docker compose -f $(DEV_COMPOSE_FILE) exec web bash

# Reiniciar contenedores
restart:
	# Detiene y vuelve a iniciar los contenedores rápidamente
	docker compose -f $(DEV_COMPOSE_FILE) restart

# Ver estado
ps:
	# Muestra una lista de los contenedores y si están corriendo o fallando
	docker compose -f $(DEV_COMPOSE_FILE) ps

# Limpiar todo (volúmenes incluidos)
clean:
	# Detiene todo y borra los volúmenes (¡Cuidado! Esto borra la base de datos)
	docker compose -f $(DEV_COMPOSE_FILE) down -v

-----

Nota: Por estándar histórico, Make requiere estrictamente el uso de tabuladores
(TAB), no espacios, para las indentaciones de los comandos.

.env
====

DB_NAME=test_django_db
DB_USER=postgres
DB_PASSWORD=123456
HOST=db
PORT=5432

-----

Aclaraciones sobre la base de datos:

La base de datos NO debe estar creada previamente, Docker Compose + PostgreSQL
se encarga de crearla automáticamente.

¿Qué hace Docker automáticamente?

Cuando usas la imagen oficial de postgres con las variables de entorno, Docker:

-Crea la base de datos automáticamente si no existe
-Crea el usuario automáticamente
-Asigna la contraseña automáticamente

yaml

environment:
  POSTGRES_DB: ${DB_NAME} # ← Crea esta BD
  POSTGRES_USER: ${DB_USER} # ← Crea o usa este usuario
  POSTGRES_PASSWORD: ${DB_PASSWORD} # ← Asigna esta contraseña

¿Qué NO hace automáticamente?

Django necesita que las tablas estén creadas. Pero eso lo haces con:

# Dentro del contenedor o en tu start.sh

$ python manage.py makemigrations person product

$ python manage.py migrate

Flujo completo (qué pasa cuando ejecutas docker compose up -d)

+-------------------+--------------------------------------------------+
| Paso              | ¿Qué sucede?                                     |
+-------------------+--------------------------------------------------+
| 1. Inicia db      | PostgreSQL crea automáticamente la BD y el       |
|                   | usuario definido en POSTGRES_DB, POSTGRES_USER   |
+-------------------+--------------------------------------------------+
| 2. Inicia web     | Django intenta conectar a la BD (usa HOST=db)    |
+-------------------+--------------------------------------------------+
| 3. start.sh       | Ejecuta makemigrations y migrate                 |
|                   | > Crea las TABLAS dentro de la BD existente      |
+-------------------+--------------------------------------------------+
| 4. runserver      | Django inicia el servidor                        |
+-------------------+--------------------------------------------------+

requirements.txt
================

Django==6.0.0
psycopg[binary]

---

Son requerimientos propios del proyecto de Django los define el desarrollador.

Probar todo lo anterior, la prueba de fuego
===========================================

Paso 1: Crear los archivos

Copia cada uno de los archivos necesarios (Dockerfile, docker-compose.yml,
Makefile, etc.) en la raíz de tu proyecto.

Paso 2: Dar permisos de ejecución a start.sh

$ chmod +x start.sh

El comando chmod +x (change mode + execute) le otorga permisos de ejecución al
script. Sin esto, Linux lo trataría como un simple archivo de texto y no
permitiría que Docker lo ejecute al iniciar el contenedor.

Paso 3: Construir y levantar los contenedores

Opción 1: Usando Make (recomendado)

$ sudo make build

Ejecuta las instrucciones del archivo Makefile. Normalmente es un atajo para
construir las imágenes personalizadas de tu proyecto basadas en el Dockerfile.

Nota: Si da un error de permission denied while trying... revisar la solución
más abajo en la parte de errores comunes y volver acá luego.

Levanta los servicios definidos en tu configuración. El sufijo -d (detached)
hace que los contenedores corran en segundo plano, liberando tu terminal para
seguir usándola.

$ sudo make up-d

Nota: Si da un error de Error response from daemon: ...host port
0.0.0.0:5432/tcp: address already in use... revisar la solución más abajo en la
parte de errores comunes y volver acá luego.

Paso 4: Verificar que todo funciona

Ver logs con Make

$ make logs

Muestra la salida por consola de lo que está ocurriendo dentro de tus
contenedores (útil para ver errores de Django o conexiones a la base de datos).

Ver logs con docker compose

$ docker compose logs -f

El parámetro -f (follow) mantiene la terminal "enganchada" a los logs,
mostrándote en tiempo real lo que sucede conforme vas usando la aplicación.

Ver contenedores activos

$ sudo make ps

Listado rápido de los contenedores del proyecto. Te permite ver el Status
(si están Up o si se reiniciaron por error) y qué Puertos están exponiendo.

Paso 5: Acceder a la aplicación

Abre tu navegador en: http://localhost:8000

----

Opción 2: En esta opción usamos comandos directos pero el resultado debe ser el
mismo, el sistema debe quedar corriendo por la url http://localhost:8000

Ejecutamos:

$ docker compose build

Lee el archivo docker-compose.yml y descarga o construye las imágenes de cada
servicio (base de datos, Python/Django, etc.).

$ docker compose up -d

Crea y arranca los contenedores. Si no existen las imágenes, las construye
primero; si ya existen, simplemente inicia los servicios.

Verificar que todo funciona: Ver logs con Make

$ make logs

Muestra la salida por consola de lo que está ocurriendo dentro de tus
contenedores (útil para ver errores de Django o conexiones a la base de datos).

Ver logs con docker compose

$ docker compose logs -f

El parámetro -f (follow) mantiene la terminal "enganchada" a los logs,
mostrándote en tiempo real lo que sucede conforme vas usando la aplicación.

Ver contenedores activos

$ sudo make ps

Listado rápido de los contenedores del proyecto. Te permite ver el Status
(si están Up o si se reiniciaron por error) y qué Puertos están exponiendo.

Acceder a la aplicación

Abre tu navegador en: http://localhost:8000

Comandos útiles
===============

1. Verificar que el contenedor de BD está corriendo

$ docker compose ps

2. Entrar a PostgreSQL dentro del contenedor

$ docker compose exec db psql -U postgres

3. Dentro de psql, listar las bases de datos
\l

4. Ver las tablas de tu BD
\c test_django_db
\dt

5. Detener y eliminar los contenedores actuales

$ docker compose down

6. Levantar todo de nuevo (esto volverá a leer el settings.py corregido)

$ make up-d

Errores comunes y soluciones
============================

1- start.sh: Permission denied

$ chmod +x start.sh

$ docker compose build

-----

2- Puerto 8000 ya en uso

Cambiar el puerto en docker-compose.yml

ports:
  - "8001:8000"  # Cambia el puerto del host

-----

3- No se puede conectar a PostgreSQL

# Asegúrate de que el HOST en .env sea "db", no "localhost"
HOST=db

-----

4- make: command not found

Instalar make en Linux

$ sudo apt install make

O usar comandos docker directamente

$ docker compose up -d

-----

5- permission denied while trying to connect to the docker API at unix:///var/run/docker.sock

Clásico error de permisos de Docker en Linux. El mensaje permission denied
indica que tu usuario actual no tiene permiso para acceder al socket de Docker
(/var/run/docker.sock), el cual, por defecto, solo es accesible para el usuario
root y los miembros del grupo docker.

Para ejecutar comandos de Docker sin usar sudo, debes añadir tu usuario al grupo
docker.

$ sudo groupadd docker

Si no existe y se crea o si indica que ya existe proceder con el siguiente
comando.

$ sudo usermod -aG docker $USER

Para que el sistema reconozca el nuevo grupo sin reiniciar, ejecuta:
  
$ newgrp docker

Verificar la creación del grupo:

$ groups

docker cdrom floppy audio dip video plugdev users netdev scanner bluetooth lpadmin my_user

6- Error response from daemon: failed to set up container networking: driver
failed programming external connectivity on endpoint django_postgres
failed to bind host port 0.0.0.0:5432/tcp: address already in use

Significa un conflicto de puertos. El error address already in use significa que
ya hay algo ocupando el puerto 5432 en la máquina Debian.

Lo más probable es que haya una instancia de PostgreSQL instalada directamente
en el sistema operativo (fuera de Docker) y se está iniciando automáticamente.

Identificar qué está usando el puerto:

$ sudo lsof -i :5432

COMMAND   PID     USER FD   TYPE DEVICE SIZE/OFF NODE NAME
postgres 1689 postgres 6u  IPv6  11882      0t0  TCP localhost:postgresql (LISTEN)
postgres 1689 postgres 7u  IPv4  11883      0t0  TCP localhost:postgresql (LISTEN)

Se confirma que tienes un servidor de PostgreSQL instalado directamente en
Debian que se está ejecutando en segundo plano y ha "secuestrado" el puerto
5432.

Como Docker intenta mapear el mismo puerto de tu computadora hacia el
contenedor, chocan entre sí.

Detén el servicio de Postgres local, ejecuta este comando para liberar el puerto
inmediatamente:

$ sudo systemctl stop postgresql

systemctl stop le dice al sistema operativo que apague el proceso postgres con
PID 1689 que viste en tu comando anterior.

Evita que vuelva a arrancar solo: Si vas a usar Docker para tus proyectos de
desarrollo, no necesitas que el Postgres nativo se inicie cada vez que prendes
la computadora:

$ sudo systemctl disable postgresql

disable quita el servicio del inicio automático, pero no desinstala nada.

Levanta tu proyecto con Docker: Ahora que el puerto está libre, el comando
debería funcionar sin problemas:

$ make up-d

7- Puerto 8000 ocupado luego de las pruebas o reiniciar¨

$ python manage.py runserver

Error: That port is already in use.

$ ps -ef | grep 8000
rabbitmq     884       1  0 02:34 ?        00:00:07 /usr/lib/erlang/erts-13.1.5/bin/beam.smp -W w -MBas ageffcbf -MHas ageffcbf -MBlmbcs 512 -MHlmbcs 512 -MMmcs 30 -P 1048576 -t 5000000 -stbt db -zdbbl 128000 -sbwt none -sbwtdcpu none -sbwtdio none -- -root /usr/lib/erlang -bindir /usr/lib/erlang/erts-13.1.5/bin -progname erl -- -home /var/lib/rabbitmq -- -pa  -noshell -noinput -s rabbit boot -boot start_sasl -syslog logger [] -syslog syslog_error_logger false -kernel prevent_overlapping_partitions false
root        2763    1764  0 02:35 ?        00:00:00 /usr/bin/docker-proxy -proto tcp -host-ip 0.0.0.0 -host-port 8000 -container-ip 172.18.0.2 -container-port 8000 -use-listen-fd
root        2778    1764  0 02:35 ?        00:00:00 /usr/bin/docker-proxy -proto tcp -host-ip :: -host-port 8000 -container-ip 172.18.0.2 -container-port 8000 -use-listen-fd
root        3419    2636  0 02:35 ?        00:00:00 python manage.py runserver 0.0.0.0:8000
root       10625    3419  1 02:45 ?        00:00:02 /usr/local/bin/python manage.py runserver 0.0.0.0:8000
aosorio    11571    4411  0 02:48 pts/0    00:00:00 grep 8000

La forma "Manual" (Si no estás en la carpeta del proyecto)

Si no estás en la carpeta Django_6_crud, puedes detenerlo directamente por su
nombre de contenedor:

$ docker stop django_app django_postgres

¿Cómo saber si ya se liberó el puerto?

Después de ejecutar cualquiera de los comandos anteriores, verifica de nuevo con
el comando que usaste antes:

$ ps -ef | grep 8000

-----

Ejemplo completo y funcional: https://github.com/argenisosorio/Django_6_crud/tree/test/deploy-docker

El archivo .dockerignore
========================

Es fundamental para que la imagen no pese gigas innecesarios, debe contener:

.git
__pycache__
*.pyc
.env
venv/

Fuentes
=======

-Fabian Palmera
-Deepseek IA
-Argenis Osorio
```
