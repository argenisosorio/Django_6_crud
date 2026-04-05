from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .forms import ConfigForm
from .models import Config


def solo_superusuario(user):
    """
    Método para saber si el usuario es superusuario.
    """
    return user.is_superuser

@login_required
@user_passes_test(solo_superusuario, login_url='registers:home')
def home(request):
    # Intentamos obtener el primer (y único) registro de configuración
    config_instance = Config.objects.first()

    if request.method == 'POST':
        form = ConfigForm(request.POST, instance=config_instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Configuración actualizada correctamente")
            return redirect('registers:home')
    else:
        form = ConfigForm(instance=config_instance)
    
    context = {
        'form': form,
        'config': config_instance
    }
    return render(request, 'configs/home.html', context)
