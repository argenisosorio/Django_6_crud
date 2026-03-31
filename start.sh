#!/bin/bash

echo "Esperando a que PostgreSQL esté listo..."
sleep 5

echo "Ejecutando migraciones..."
python manage.py makemigrations person product --no-input
python manage.py migrate --no-input

echo "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000