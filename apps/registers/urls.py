from django.urls import path
from . import views


app_name = 'registers'


urlpatterns = [
    path('', views.home, name='home'),
    path('create_update_register/', views.create_update_register, name='create_update_register'),
    #path('<int:pk>/', views.detail_register, name='detail'),
    #path('<int:pk>/update/', views.update_register, name='update'),
    #path('<int:pk>/delete/', views.delete_register, name='delete'),
]
