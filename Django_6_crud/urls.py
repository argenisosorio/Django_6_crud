from django.contrib import admin
from django.urls import include, path
from django.conf.urls import handler404


# URL para el error 404 y 500 personalizados.
handler404 = 'apps.person.views.error_404'
handler500 = 'apps.person.views.error_500'


urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Include the URLs from person app.
    path('', include('apps.person.urls')),

    # Include the URLs from product app.
    path('products/', include('apps.product.urls')),
]
