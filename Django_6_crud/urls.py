from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    # Admin route
    path('darkmagician/', admin.site.urls),

    # Redirigir la raíz al login de users
    path('', lambda request: redirect('users:login'), name='root'),

    # Include the URLs from product app.
    path('registers/', include('apps.registers.urls')),

    # Include the URLs from users app.
    path('users/', include('apps.users.urls')),

    # Include the URLs from configs app.
    path('configs/', include('apps.configs.urls')),
]
