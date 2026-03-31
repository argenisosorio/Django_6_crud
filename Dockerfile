FROM python:3.12-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos primero (mejora la caché)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Dar permisos de ejecución al script start.sh
RUN chmod +x start.sh

# Exponer el puerto de Django
EXPOSE 8000

# Comando para ejecutar el contenedor
CMD ["./start.sh"]