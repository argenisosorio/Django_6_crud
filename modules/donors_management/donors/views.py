from django.shortcuts import render, redirect, get_object_or_404
from .models import Donor
from .forms import DonorForm


def home(request):
    donors = Donor.objects.all()
    context = {
        'donors': donors,
        'message': '¡Hello Donors!',
    }
    return render(request, 'donors/home.html', context)

def create_donor(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donors:home')
    else:
        form = DonorForm()
    
    context = {'form': form}
    return render(request, 'donors/create.html', context)

def detail_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    context = {'donor': donor}
    return render(request, 'donors/detail.html', context)

def update_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('donors:detail', pk=donor.pk)
    else:
        form = DonorForm(instance=donor)
    
    context = {'form': form, 'donor': donor}
    return render(request, 'donors/update.html', context)


def delete_donor(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor.delete()
        return redirect('donors:home')
    
    context = {'donor': donor}
    return render(request, 'donors/delete.html', context)
