from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin route
    path('admin/', admin.site.urls),

    # Include the URLs from persons app.
    path('', include('apps.persons.urls')),

    # Include the URLs from product app.
    path('products/', include('apps.product.urls')),
]
