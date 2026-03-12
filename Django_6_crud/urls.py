from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Include the URLs from person app.
    path('', include('apps.person.urls')),

    # Include the URLs from product app.
    path('products/', include('apps.product.urls')),
]

# Servir archivos media en modo desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
