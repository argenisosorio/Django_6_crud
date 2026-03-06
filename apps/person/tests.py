from django.test import TestCase
from .models import Person
from django.core.exceptions import ValidationError

class PersonModelTest(TestCase):
    def setUp(self):
        self.person = Person.objects.create(
            name='Pedro',
            email='[EMAIL_ADDRESS]',
            age=30
        )

    def test_person_creation(self):
        """🟦 Verifica que la persona se cree correctamente"""
        self.assertEqual(self.person.name, 'Pedro')
        self.assertEqual(self.person.email, '[EMAIL_ADDRESS]')
        self.assertEqual(self.person.age, 30)

    def test_person_str(self):
        """🟦 Verifica que el método __str__ devuelva el nombre"""
        self.assertEqual(str(self.person), 'Pedro')

    def test_negative_age_fails(self):
        """🟦 Verifica que no se permitan edades negativas"""
        invalid_person = Person(name="Error", email="[EMAIL_ADDRESS]", age=-10)

        with self.assertRaises(ValidationError):
            invalid_person.full_clean()

    def test_invalid_email_format_fails(self):
        """🟦 Verifica que el EmailField detecte correos invalidos"""
        invalid_person = Person(name="Error", email="esto_no_es_un_correo", age=20)

        with self.assertRaises(ValidationError):
            invalid_person.full_clean()

    def test_name_too_long_fails(self):
        """🟦 Verifica la restricción de max_length=100"""
        nombre_largo = "A" * 101
        invalid_person = Person(name=nombre_largo, email="[EMAIL_ADDRESS]", age=25)

        with self.assertRaises(ValidationError):
            invalid_person.full_clean()
