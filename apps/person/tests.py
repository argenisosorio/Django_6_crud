from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Person

class PersonModelTest(TestCase):
    """
    Pruebas unitarias para la validación y creación del modelo Person.
    Este conjunto de pruebas asegura la integridad de los datos de los ciudadanos
    en el sistema bajo estándares de excelencia técnica.
    """

    def setUp(self):
        """
        Configuración inicial de la prueba.
        El método setUp se ejecuta antes de cada prueba y es el que nos permite
        crear una instancia del modelo. En este caso, creamos una persona con
        nombre "Pedro", email "pedro@ejemplo.com" y edad 30. Esta persona se usará en
        las pruebas posteriores para verificar el comportamiento del modelo.
        """
        self.person = Person.objects.create(
            name='Pedro',
            email='pedro@ejemplo.com',
            age=30
        )

    def test_person_creation(self):
        """
        Verifica la persistencia correcta de los atributos del modelo.
        Los métodos de prueba deben comenzar con "test_". En este caso será un test
        de afirmación y debemos usar self.assert* para verificar que la prueba sea
        correcta, comparando valores reales con valores esperados.
        """
        # Verifica que la persona se cree y recupere correctamente
        self.assertEqual(self.person.name, 'Pedro')
        self.assertEqual(self.person.email, 'pedro@ejemplo.com')
        self.assertEqual(self.person.age, 30)

    def test_negative_age_fails(self):
        """
        Valida que el sistema restrinja datos inconsistentes (edades negativas).
        En este caso será un test de excepción (se usa ValidationError)
        y usamos assertRaises para verificar que se lance una ValidationError.
        full_clean() es un método que valida el modelo manualmente antes de guardar.
        """
        # CORRECCIÓN: Se usa un email válido para que Django no falle por el correo
        # y permita que la validación llegue al campo 'age'.
        invalid_person = Person(name="Error", email="error@ejemplo.com", age=-10)

        """
        Verifica que se lance una ValidationError al intentar validar una
        persona con edad negativa, asegurando que el error provenga del campo 'age'.
        """
        with self.assertRaises(ValidationError) as context:
            invalid_person.full_clean()

        # Validación adicional: se confirma que el error está en el campo específico
        self.assertIn('age', context.exception.message_dict)

    def test_email_uniqueness(self):
        """
        Verifica la restricción de unicidad para el correo electrónico.
        Garantiza que no existan registros duplicados en la base de datos,
        manteniendo la integridad de la información.
        """
        # Se intenta crear una persona con el mismo email que el objeto de setUp
        duplicate_person = Person(name="Juan", email='pedro@ejemplo.com', age=25)
        with self.assertRaises(ValidationError):
            duplicate_person.full_clean()
