from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Donation
from .forms import DonationForm


def create_donation(request):
    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.donor = request.user
            donation.save()
            return redirect('my_donations')
    else:
        form = DonationForm()
    return render(request, 'donations/create_donation.html', {'form': form})

def my_donations(request):
    donations = Donation.objects.all()
    return render(request, 'donations/my_donations.html', {'donations': donations})


def donation_detail(request, pk):
    donation = Donation.objects.get(pk=pk)
    return render(request, 'donations/donation_detail.html', {'donation': donation})

def update_donation(request, pk):
    donation = Donation.objects.get(pk=pk)

    if request.method == 'POST':
        donation.title = request.POST.get('title')
        donation.category = request.POST.get('category')
        donation.quantity = request.POST.get('quantity')
        donation.description = request.POST.get('description')
        donation.pickup_address = request.POST.get('pickup_address')
        donation.city = request.POST.get('city')

        expiration_date = request.POST.get('expiration_date')
        if expiration_date:
            donation.expiration_date = expiration_date

        if request.FILES.get('image'):
            donation.image = request.FILES.get('image')

        donation.save()
        return redirect('my_donations')

    return render(request, 'donations/update_donation.html', {'donation': donation})

def delete_donation(request, pk):
    donation = Donation.objects.get(pk=pk)
    if request.method == 'POST':
        donation.delete()
        return redirect('my_donations')
    return render(request, 'donations/delete_donation.html', {'donation': donation})
