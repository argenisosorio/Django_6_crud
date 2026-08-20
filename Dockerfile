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
