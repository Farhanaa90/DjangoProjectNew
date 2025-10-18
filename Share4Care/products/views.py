from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Donation
from .forms import DonationForm
from users.models import UserProfile


@login_required
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

        donation = Donation.objects.create(
            donor=request.user,
            title=title,
            category=category,
            quantity=quantity,
            description=description,
            pickup_address=pickup_address,
            city=city,
            expiration_date=expiration_date if expiration_date else None,
            image=image if image else None
        )

        return redirect('my_donations')

    return render(request, 'donations/create_donation.html')


@login_required
def my_donations(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.user_type != 'donor':
        messages.error(request, 'Only donors can view donations!')
        return redirect('dashboard')

    donations = Donation.objects.filter(donor=request.user).order_by('-created_at')
    return render(request, 'donations/my_donations.html', {'donations': donations})


@login_required
def donation_detail(request, pk):
    donation = get_object_or_404(Donation, pk=pk)
    return render(request, 'donations/donation_detail.html', {'donation': donation})


@login_required
def update_donation(request, pk):
    donation = Donation.objects.get(pk=pk, donor=request.user)

    if request.method == 'POST':
        form = DonationForm(request.POST, request.FILES, instance=donation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Donation updated successfully!')
            return redirect('my_donations')
    else:
        form = DonationForm(instance=donation)

    return render(request, 'donations/update_donation.html', {'form': form, 'donation': donation})


@login_required
def delete_donation(request, pk):
    donation = get_object_or_404(Donation, pk=pk, donor=request.user)

    if request.method == 'POST':
        donation.delete()
        messages.success(request, 'Donation deleted successfully!')
        return redirect('my_donations')

    return render(request, 'donations/delete_donation.html', {'donation': donation})