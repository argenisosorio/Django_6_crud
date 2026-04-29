from django.urls import path
from . import views
from apps.registers.views import (
    RegisterDetailView
)


app_name = 'registers'


urlpatterns = [
    path('', views.home, name='home'),
    path('create_update_register/', views.create_update_register, name='create_update_register'),
    path('list/', views.list, name='list'),
    path('<int:pk>/update_points/', views.update_points, name='update_points'),
    path('ranking', views.ranking, name='ranking'),
    # Detalles de la quiniela de un jugador específico.
    path(
        "<int:pk>/",
        RegisterDetailView.as_view(template_name="registers/register_detail.html"),
        name="register_detail"
    ),
]
