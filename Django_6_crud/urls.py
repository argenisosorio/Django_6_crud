from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI
# Importamos el router de la app person
from apps.person.api import router as person_router

# 1. Instanciamos la API
api = NinjaAPI(title="Mi Proyecto CRUD API")

# 2. Añadimos los routers de cada app (puedes añadir el de products luego)
api.add_router("/person/", person_router)

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Tus rutas de templates/vistas tradicionales
    path('', include('apps.person.urls')),
    path('products/', include('apps.product.urls')),

    # 3. La ruta para TODA la API y su documentación
    path("api/", api.urls),
]
