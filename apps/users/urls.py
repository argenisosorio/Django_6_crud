from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from apps.users import views
from apps.users.views import (
    SignUpView,
    UserCreateView,
    UserDeleteView,
    UserDetailView,
    UserListView,
    UserUpdateView,
    ProfileUpdateView,
    UpdateActiveUserView,
)

app_name = "users"

urlpatterns = [
    # URL de login.
    path(
        "login/",
        views.LoginView.as_view(template_name="users/login.html"),
        name="login"
    ),
    # URL de logout.
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout"
    ),
    # URL de registro de nuevos usuarios (signup)
    path(
        "signup/",
        SignUpView.as_view(template_name="users/signup.html"),
        name="signup"
    ),

    # URL de Actualización de usuarios para el Administrador.
    path(
        "profile_update/<int:pk>/",
        ProfileUpdateView.as_view(template_name="users/profile_form.html"),
        name="profile_update"
    ),

    # Urls de recuperación de contraseña
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(
            template_name="users/password_reset_form.html",
            email_template_name="users/password_reset_email.html",
            html_email_template_name="users/password_reset_email.html",
            success_url=reverse_lazy("users:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="users/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="users/password_reset_confirm.html",
            success_url=reverse_lazy("users:password_reset_complete")
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="users/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),

    # URL de cambio de contraseña (para usuarios autenticados)
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="users/password_change_form.html",
            success_url=reverse_lazy("users:password_change_done")
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="users/password_change_done.html"
        ),
        name="password_change_done",
    ),

    # URL de Listado de usuarios para el Administrador.
    path(
        "",
        UserListView.as_view(template_name="users/user_list.html"),
        name="user_list"
    ),
    # URL de Detalle de usuario para el Administrador.
    path(
        "<int:pk>/",
        UserDetailView.as_view(template_name="users/user_detail.html"),
        name="user_detail"
    ),
    # URL de Registro de nuevos usuarios para el Administrador.
    path(
        "create/",
        UserCreateView.as_view(template_name="users/user_form.html"),
        name="user_create"
    ),
    # URL de Actualización de usuarios para el Administrador.
    path(
        "update/<int:pk>/",
        UserUpdateView.as_view(template_name="users/user_form.html"),
        name="user_update"
    ),
    # URL de Eliminación de usuarios para el Administrador.
    path(
        "delete/<int:pk>/",
        UserDeleteView.as_view(template_name="users/user_confirm_delete.html"),
        name="user_delete"
    ),
    # URL de Actualización del estado activo de usuarios para el Administrador.
    path(
        "update_user_active/<int:pk>/",
        UpdateActiveUserView.as_view(template_name="users/update_active_user_form.html"),
        name="update_active_user"
    ),
]