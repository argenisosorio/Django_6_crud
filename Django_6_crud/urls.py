from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Redirigir la raíz al login de users
    path('', lambda request: redirect('users:login'), name='root'),

    # Include the URLs from person app.
    path('person/', include('apps.person.urls')),

    # Include the URLs from product app.
    path('products/', include('apps.product.urls')),

    # Include the URLs from users app.
    path('users/', include('apps.users.urls')),
]