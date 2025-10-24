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

def browse_donations(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.user_type == 'donor':
        messages.error(request, 'Only collectors can browse donations!')
        return redirect('dashboard')

    donations = Donation.objects.filter(status='available')

    return render(request, 'collectors/browse_donations.html', {'donations': donations})

def claim_donation(request, pk):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.user_type == 'donor':
        messages.error(request, 'Only collectors can claim donations!')
        return redirect('dashboard')

    donation = Donation.objects.get(pk=pk)

    if donation.status != 'available':
        messages.error(request, 'This donation is not available!')
        return redirect('browse_donations')

    existing_claim = DonationClaim.objects.filter(donation=donation, collector=request.user).first()
    if existing_claim:
        messages.error(request, 'You have already claimed this donation!')
        return redirect('my_claims')

    if request.method == 'POST':
        message_text = request.POST.get('message')

        claim = DonationClaim.objects.create(
            donation=donation,
            collector=request.user,
            message=message_text,
            status='pending'
        )

        Notification.objects.create(
            user=donation.donor,
            message=f"{request.user.username} wants to collect your donation: {donation.title}",
            claim_id=claim.id,
            is_read=False
        )

        messages.success(request, 'Donation claimed successfully!')
        return redirect('my_claims')

    return render(request, 'collectors/claim_donation.html', {'donation': donation})

def my_claims(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.user_type == 'donor':
        messages.error(request, 'Only collectors can view claims!')
        return redirect('dashboard')

    claims = DonationClaim.objects.filter(collector=request.user)
    return render(request, 'collectors/my_claims.html', {'claims': claims})

def cancel_claim(request, pk):
    claim = DonationClaim.objects.get(pk=pk)

    if claim.collector == request.user:
        if claim.status == 'pending':
            claim.delete()
            messages.success(request, 'Claim cancelled successfully!')
        else:
            messages.error(request, 'Cannot cancel this claim!')

    return redirect('my_claims')

def donation_claims(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if user_profile.user_type == 'collector':
        messages.error(request, 'Only donors can view claims!')
        return redirect('dashboard')

    claims = DonationClaim.objects.filter(donation__donor=request.user)
    return render(request, 'donations/donation_claims.html', {'claims': claims})

def approve_claim(request, pk):
    claim = DonationClaim.objects.get(pk=pk)

    if claim.donation.donor == request.user:
        if claim.status == 'pending':
            claim.status = 'approved'
            claim.save()

            claim.donation.status = 'claimed'
            claim.donation.save()

            Notification.objects.create(
                user=claim.collector,
                message=f"Your request for '{claim.donation.title}' has been approved! You can collect it now.",
                claim_id=claim.id,
                is_read=False
            )

            messages.success(request, 'Claim approved successfully!')
        else:
            messages.error(request, 'This claim has already been processed!')

    return redirect('donation_claims')

def reject_claim(request, pk):
    claim = DonationClaim.objects.get(pk=pk)

    if claim.donation.donor == request.user:
        if claim.status == 'pending':
            claim.status = 'rejected'
            claim.save()

            Notification.objects.create(
                user=claim.collector,
                message=f"Your request for '{claim.donation.title}' has been rejected.",
                claim_id=claim.id,
                is_read=False
            )

            messages.success(request, 'Claim rejected successfully!')
        else:
            messages.error(request, 'This claim has already been processed!')

    return redirect('donation_claims')