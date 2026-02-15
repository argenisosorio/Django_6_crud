from rest_framework import viewsets
from .models import Person
from .serializers import PersonSerializer

class PersonViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver, editar o eliminar personas.
    """
    queryset = Person.objects.all().order_by('-created_at')
    serializer_class = PersonSerializer
