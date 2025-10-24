from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, Message


def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_type = request.POST.get('user_type')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name
        )

        UserProfile.objects.create(
            user=user,
            user_type=user_type
        )

        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('dashboard')

    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'dashboard.html', {'user_profile': user_profile})

def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'user_profile': user_profile})

def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        request.user.first_name = request.POST.get('name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()

        user_profile.phone = request.POST.get('phone', '')
        user_profile.city = request.POST.get('city', '')
        user_profile.address = request.POST.get('address', '')

        if request.FILES.get('profile_picture'):
            user_profile.profile_picture = request.FILES['profile_picture']

        user_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'users/edit_profile.html', {'user_profile': user_profile})

def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(old_password):
            messages.error(request, 'Current password is incorrect!')
            return render(request, 'change_password.html')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match!')
            return render(request, 'change_password.html')

        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user)

        messages.success(request, 'Password changed successfully!')
        return redirect('dashboard')

    return render(request, 'change_password.html')

def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully!')
        return redirect('home')

    return render(request, 'delete_account.html')

def send_message(request, user_id):
    receiver = User.objects.get(id=user_id)

    if request.method == 'POST':
        subject = request.POST.get('subject')
        content = request.POST.get('content')

        Message.objects.create(
            sender=request.user,
            receiver=receiver,
            subject=subject,
            content=content
        )

        messages.success(request, 'Message sent successfully!')
        return redirect('inbox')

    return render(request, 'messages/send_message.html', {'receiver': receiver})

def inbox(request):
    received_messages = Message.objects.filter(receiver=request.user)
    unread_count = Message.objects.filter(receiver=request.user, is_read=False).count()

    return render(request, 'messages/inbox.html', {'messages': received_messages, 'unread_count': unread_count})

def sent_messages(request):
    sent_msgs = Message.objects.filter(sender=request.user)
    return render(request, 'messages/sent_messages.html', {'messages': sent_msgs})

def view_message(request, pk):
    message = Message.objects.get(pk=pk)

    if message.receiver == request.user:
        if message.is_read == False:
            message.is_read = True
            message.save()

    return render(request, 'messages/view_message.html', {'message': message})

def message_detail(request, pk):
    message = Message.objects.get(pk=pk)

    if message.receiver == request.user:
        if message.is_read == False:
            message.is_read = True
            message.save()

    return render(request, 'messages/message_detail.html', {'message': message})

def delete_message(request, pk):
    message = Message.objects.get(pk=pk)

    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Message deleted successfully!')
        return redirect('inbox')

    return render(request, 'messages/delete_message.html', {'message': message})
