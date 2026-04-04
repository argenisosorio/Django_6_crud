from django.urls import path
from . import views


app_name = 'registers'


urlpatterns = [
    path('', views.home, name='home'),
    path('create_update_register/', views.create_update_register, name='create_update_register'),
    path('list/', views.list, name='list'),
    path('config/', views.config, name='config'),
    path('<int:pk>/update_points/', views.update_points, name='update_points'),
    #path('<int:pk>/', views.detail_register, name='detail'),
    #path('<int:pk>/delete/', views.delete_register, name='delete'),
]
