from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Message


class RegistrationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())
    user_type = forms.ChoiceField(choices=[('donor', 'Donor'), ('collector', 'Collector')])

    class Meta:
        model = User
        fields = ['name', 'email', 'username', 'password', 'user_type']


class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'content']