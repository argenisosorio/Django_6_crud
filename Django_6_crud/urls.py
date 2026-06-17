from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    # Admin route
    path('cen-com/', admin.site.urls),

    # Redirigir la raíz al login de users
    path('', lambda request: redirect('users:login'), name='root'),

    # Include the URLs from users app.
    path('users/', include('apps.users.urls')),

    path('requests/', include('apps.requests.urls')),

    path('registers_local/', include('apps.registers_local.urls')),

    path('registers_extern/', include('apps.registers_extern.urls')),
]