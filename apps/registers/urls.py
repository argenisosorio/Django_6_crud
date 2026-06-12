from django.urls import path
from . import views
from apps.registers.views import (
    RegisterDetailView,
    RegisterDetailPubView,
    RegisterDetailViewForAdmin
)


app_name = 'registers'


urlpatterns = [
    path('', views.home, name='home'),
    path('create_update_register/', views.create_update_register, name='create_update_register'),
    path('list/', views.list, name='list'),
    path('<int:pk>/update_points/', views.update_points, name='update_points'),
    path('ranking', views.ranking, name='ranking'),
    path('ranking_pub', views.ranking_pub, name='ranking_pub'),
    path('ranking_for_admin', views.ranking_for_admin, name='ranking_for_admin'),
    path('groups', views.groups, name='groups'),
    path('results', views.results, name='results'),
    # Detalles de la quiniela de un jugador específico.
    #path(
        #"<int:pk>/",
        #RegisterDetailView.as_view(template_name="registers/register_detail.html"),
        #name="register_detail"
    #),

    # Detalles de la quiniela de un jugador específico.
    path(
        "<int:pk>/",
        RegisterDetailPubView.as_view(template_name="registers/register_detail_pub.html"),
        name="register_detail_pub"
    ),
    # Detalles de la quiniela de un jugador específico para el admin.
    path(
        "admin/<int:pk>/",
        RegisterDetailViewForAdmin.as_view(template_name="registers/register_detail_for_admin.html"),
        name="register_detail_for_admin"
    ),
]
