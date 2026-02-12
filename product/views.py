from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm

class ProductListView(ListView):
    """Displays the product list"""
    model = Product
    template_name = 'product/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = '¡Hello Django 6 Product CRUD!'
        return context

class ProductDetailView(DetailView):
    """Shows product details"""
    model = Product
    template_name = 'product/detail.html'
    context_object_name = 'product'

class ProductCreateView(CreateView):
    """Display the form and create a product"""
    model = Product
    form_class = ProductForm
    template_name = 'product/create.html'
    success_url = reverse_lazy('product:home')

class ProductUpdateView(UpdateView):
    """Display the form and update a product"""
    model = Product
    form_class = ProductForm
    template_name = 'product/update.html'
    
    def get_success_url(self):
        return reverse_lazy('product:detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(DeleteView):
    """Confirm and delete a product"""
    model = Product
    template_name = 'product/delete.html'
    success_url = reverse_lazy('product:home')
