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
