from django.contrib.auth import get_user_model, login, logout
from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as AuthLoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)


class LoginView(AuthLoginView):
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        """Redirigir a Home después de iniciar sesión exitosamente."""
        return reverse_lazy("registers:home")


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("users:login")

    def post(self, request):
        logout(request)
        return redirect("users:login")


class SignUpView(CreateView):
    model = get_user_model()
    template_name = "users/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("registers:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class UserListView(LoginRequiredMixin, ListView):
    model = get_user_model()
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = "users/user_detail.html"
    context_object_name = "user"


class UserCreateView(LoginRequiredMixin, CreateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("users:user_list")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "users/user_form.html"
    form_class = CustomUserChangeForm
    success_url = reverse_lazy("users:user_list")


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:user_list")
