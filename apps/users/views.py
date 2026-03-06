from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


class UserListView(ListView):
    model = User
    template_name = "users/user_list.html"
    context_object_name = "users"


class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"
    context_object_name = "user"


class UserCreateView(CreateView):
    model = User
    template_name = "users/user_form.html"
    fields = ["username", "email", "first_name", "last_name"]
    success_url = reverse_lazy("users:user_list")


class UserUpdateView(UpdateView):
    model = User
    template_name = "users/user_form.html"
    fields = ["username", "email", "first_name", "last_name"]
    success_url = reverse_lazy("users:user_list")


class UserDeleteView(DeleteView):
    model = User
    template_name = "users/user_confirm_delete.html"
    success_url = reverse_lazy("users:user_list")
