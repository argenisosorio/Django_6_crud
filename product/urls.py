from django.urls import path
from . import views

# Define the application namespace for URL reversing
# This helps distinguish URLs between different apps when using 'url' template tag
app_name = 'product'

# URL patterns for the Product CRUD (Create, Read, Update, Delete) operations
urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('create/', views.ProductCreateView.as_view(), name='create'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.ProductUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.ProductDeleteView.as_view(), name='delete'),
]
