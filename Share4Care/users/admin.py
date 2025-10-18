from django.contrib import admin
from .models import UserProfile, ContactMessage

admin.site.register(UserProfile)
admin.site.register(ContactMessage)