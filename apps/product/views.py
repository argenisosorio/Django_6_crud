from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm
from django.contrib.auth.mixins import PermissionRequiredMixin


class ProductListView(PermissionRequiredMixin, ListView):
    """Displays the product list"""
    model = Product
    template_name = 'product/home.html'
    context_object_name = 'products'

    # Permiso requerido
    permission_required = 'product.list_products'

    # Lanza 403 HTTP Forbidden si no tiene el permiso
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = '¡Hello Django 6 Product CRUD!'
        return context


class ProductDetailView(PermissionRequiredMixin, DetailView):
    """Shows product details"""
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'

    # Permiso requerido
    permission_required = 'product.view_product'

    # Lanza 403 HTTP Forbidden si no tiene el permiso
    raise_exception = True


class ProductCreateView(PermissionRequiredMixin, CreateView):
    """Display the form and create a product"""
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product:home')

    # Permiso requerido
    permission_required = 'product.add_product'

    # Lanza 403 HTTP Forbidden si no tiene el permiso
    raise_exception = True


class ProductUpdateView(PermissionRequiredMixin, UpdateView):
    """Display the form and update a product"""
    model = Product
    form_class = ProductForm
    template_name = 'product/update.html'

    # Permiso requerido
    permission_required = 'product.change_product'

    # Lanza 403 HTTP Forbidden si no tiene el permiso
    raise_exception = True

    def get_success_url(self):
        return reverse_lazy('product:detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(PermissionRequiredMixin, DeleteView):
    """Confirm and delete a product"""
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('product:home')

    # Permiso requerido
    permission_required = 'product.delete_product'

    # Lanza 403 HTTP Forbidden si no tiene el permiso
    raise_exception = True
