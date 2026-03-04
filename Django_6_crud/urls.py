from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Include the URLs from persons app.
    path('', include('apps.persons.urls')),
]
