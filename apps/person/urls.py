from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PersonViewSet

router = DefaultRouter()
router.register(r'', PersonViewSet) # Esto crea las rutas automáticas

urlpatterns = [
    path('', include(router.urls)),
]