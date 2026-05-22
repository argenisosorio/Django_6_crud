"""
Este comando personalizado de Django imprime un mensaje amigable "Hola Mundo" en
la terminal.
"""

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Comando personalizado para imprimir "Hola Mundo" en la terminal.

    Attributes:
        help (str): Descripción del comando que de ayuda.

    Methods:
        handle(self, *args, **options): Método principal que se ejecuta cuando
        se llama al comando.

    Example:
        Para ejecutar este comando, use el siguiente comando en la terminal:
            python manage.py holamundo

        Para ejecutar este comando con la ayuda de Django, use:
            python manage.py help
    """
    # Descripción del comando para la ayuda de Django
    # El atributo 'help' proporciona una descripción breve del comando que se
    # muestra cuando se ejecuta `python manage.py help`.
    help = "Imprime un amigable Hola Mundo en la terminal"

    def handle(self, *args, **options):
        # Usamos self.stdout.write en lugar de print() 
        # para que Django maneje correctamente los colores y la salida de datos
        #self.stdout.write(self.style.SUCCESS("¡Hola Mundo desde Django 6!"))
        print("¡Hola Mundo desde Django 6!")
