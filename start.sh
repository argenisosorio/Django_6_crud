#!/bin/bash

# Función para esperar a la base de datos
# Usamos las variables de entorno que ya tienes definidas en el docker-compose
echo "----- Esperando a que PostgreSQL esté listo en el host: $DB_HOST..."

until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"
do
  echo "----- Postgres aún no responde... reintentando en 2 segundos"
  sleep 2
done

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