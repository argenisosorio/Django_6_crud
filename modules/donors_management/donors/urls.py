from django.urls import path
from . import views


app_name = 'donors'


urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_donor, name='create'),
    path('<int:pk>/', views.detail_donor, name='detail'),
    path('<int:pk>/update/', views.update_donor, name='update'),
    path('<int:pk>/delete/', views.delete_donor, name='delete'),
]
