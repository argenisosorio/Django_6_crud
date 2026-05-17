from django.urls import path
from . import views


app_name = 'registers_extern'


urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_register, name='create'),
    path('<int:pk>/', views.detail_register, name='detail'),
    path('<int:pk>/update/', views.update_register, name='update'),
    path('<int:pk>/delete/', views.delete_register, name='delete'),
    # path('exportar/excel/', views.export_registers_excel, name='export_excel'),
]
