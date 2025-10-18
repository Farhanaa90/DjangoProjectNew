from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_donations, name='my_donations'),
    path('create/', views.create_donation, name='create_donation'),
    path('<int:pk>/', views.donation_detail, name='donation_detail'),
    path('<int:pk>/edit/', views.update_donation, name='update_donation'),
    path('<int:pk>/delete/', views.delete_donation, name='delete_donation'),
]