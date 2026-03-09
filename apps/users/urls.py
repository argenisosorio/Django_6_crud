from django.urls import path
from apps.users import views
from apps.users.views import (
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserUpdateView,
)

app_name = "users"

urlpatterns = [
    # URLs de autenticación
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # Urls CRUD de usuarios
    path("", UserListView.as_view(), name="user_list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("create/", UserCreateView.as_view(), name="user_create"),
    path("update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
]
