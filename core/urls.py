# core/urls.py
from django.urls import path
from .views import DonationListCreate, RequestListCreate, RegisterAPI

urlpatterns = [
    path('donations/', DonationListCreate.as_view(), name='api_donations'),
    path('requests/', RequestListCreate.as_view(), name='api_requests'),
    path('register/', RegisterAPI.as_view(), name='api_register'),
]