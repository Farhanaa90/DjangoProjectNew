from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_donations, name='my_donations'),
    path('create/', views.create_donation, name='create_donation'),
    path('<int:pk>/', views.donation_detail, name='donation_detail'),
    path('<int:pk>/edit/', views.update_donation, name='update_donation'),
    path('<int:pk>/delete/', views.delete_donation, name='delete_donation'),
    path('browse/', views.browse_donations, name='browse_donations'),
    path('<int:pk>/claim/', views.claim_donation, name='claim_donation'),
    path('my-claims/', views.my_claims, name='my_claims'),
    path('claims/<int:pk>/cancel/', views.cancel_claim, name='cancel_claim'),
    path('claims/', views.donation_claims, name='donation_claims'),
    path('claims/<int:pk>/approve/', views.approve_claim, name='approve_claim'),
    path('claims/<int:pk>/reject/', views.reject_claim, name='reject_claim'),
]