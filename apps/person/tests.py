from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Person

class PersonModelTest(TestCase):
    """Pruebas unitarias para la validación y creación del modelo Person."""

    def setUp(self):
        """Configuración inicial para las pruebas de integridad de datos."""
        self.person = Person.objects.create(
            name='Pedro',
            email='[EMAIL_ADDRESS]',
            age=30
        )

    def test_person_creation(self):
        """Verifica que los atributos del modelo se asignen y persistan correctamente."""
        self.assertEqual(self.person.name, 'Pedro')
        self.assertEqual(self.person.email, '[EMAIL_ADDRESS]')
        self.assertEqual(self.person.age, 30)

    def test_negative_age_validation_fails(self):
        """Verifica que el modelo restrinja edades negativas mediante full_clean()."""
        person_invalid_age = Person(name="Error", email="[EMAIL_ADDRESS]", age=-10)

        # Se captura la excepción para inspeccionar los errores por campo
        with self.assertRaises(ValidationError) as context:
            person_invalid_age.full_clean()

        # Mejora: Verificar que el error esté específicamente en el campo 'age'
        self.assertIn('age', context.exception.message_dict)

    def test_email_uniqueness(self):
        """Prueba adicional: Verifica que no se permitan correos duplicados si el modelo lo requiere."""
        duplicate_person = Person(name="Juan", email='[EMAIL_ADDRESS]', age=25)
        with self.assertRaises(ValidationError):
            duplicate_person.full_clean()
