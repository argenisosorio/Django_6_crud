from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Redirigir la raíz al login de users
    path('', lambda request: redirect('users:login'), name='root'),

    # Include the URLs from users app.
    path('modules/users_management/users/', include('modules.users_management.users.urls')),

    # Include the URLs from donors app.
    path('modules/donors_management/donors/', include('modules.donors_management.donors.urls')),
]