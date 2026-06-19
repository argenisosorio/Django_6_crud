from django.urls import path
from . import views


app_name = 'registers'


urlpatterns = [
    path('', views.home, name='home'),
]
