from django.urls import path
from . import views

urlpatterns = [
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/mark-as-read/<int:pk>/', views.mark_as_read, name='mark_as_read'),
    path('notifications/delete/<int:pk>/', views.delete_notification, name='delete_notification'),
    path('notifications/accept/<int:pk>/', views.accept_claim_notification, name='accept_claim_notification'),

]