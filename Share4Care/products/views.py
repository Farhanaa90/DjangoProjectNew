from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Donation, DonationClaim
from users.models import UserProfile
from user_details.models import Notification


def create_donation(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        quantity = request.POST.get('quantity')
        description = request.POST.get('description')
        pickup_address = request.POST.get('pickup_address')
        city = request.POST.get('city')
        expiration_date = request.POST.get('expiration_date')
        image = request.FILES.get('image')

        Donation.objects.create(
            donor=request.user,
            title=title,
            category=category,
            quantity=quantity,
            description=description,
            pickup_address=pickup_address,
            city=city,
            expiration_date=expiration_date if expiration_date else None,
            image=image
        )

        messages.success(request, 'Donation created successfully!')
        return redirect('my_donations')

    return render(request, 'donations/create_donation.html')

def my_donations(request):
    donations = Donation.objects.filter(donor=request.user)
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
        messages.success(request, 'Donation updated successfully!')
        return redirect('my_donations')

    return render(request, 'donations/update_donation.html', {'donation': donation})

def delete_donation(request, pk):
    donation = Donation.objects.get(pk=pk)

    if request.method == 'POST':
        donation.delete()
        messages.success(request, 'Donation deleted successfully!')
        return redirect('my_donations')

    return render(request, 'donations/delete_donation.html', {'donation': donation})