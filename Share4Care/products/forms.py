from django import forms
from products.models import Donation

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'description', 'category', 'quantity', 'pickup_address', 'city', 'expiration_date', 'image']