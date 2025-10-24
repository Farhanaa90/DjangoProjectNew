from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification
from products.models import DonationClaim

def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user)
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()

    return render(request, 'notifications/notifications.html', {
        'notifications': user_notifications,
        'unread_count': unread_count
    })

def mark_as_read(request, pk):
    notification = Notification.objects.get(pk=pk)

    if notification.user == request.user:
        notification.is_read = True
        notification.save()

    return redirect('notifications')

def delete_notification(request, pk):
    notification = Notification.objects.get(pk=pk)

    if notification.user == request.user:
        notification.delete()

    return redirect('notifications')

def accept_claim_notification(request, pk):
    notification = Notification.objects.get(pk=pk)

    if notification.user == request.user:
        claim = DonationClaim.objects.get(pk=notification.claim_id)

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

                notification.is_read = True
                notification.save()
                messages.success(request, 'Request accepted!')
            else:
                messages.error(request, 'This claim has already been processed!')
        else:
            messages.error(request, 'You are not authorized to accept this claim!')
    return redirect('notifications')