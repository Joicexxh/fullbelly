# core/urls.py
from django.urls import path
from .views import (
    index,
    register_user,
    DonationListCreate,
    DonationDetail,
    RequestListCreate,
    RequestDetail,
    UserList,
    UserDetail,
)

urlpatterns = [
    # Index (últimas 10 doações)
    path('', index, name='api_index'),

    # Registro de usuário
    path('register/', register_user, name='api_register'),

    # Doações
    path('donations/', DonationListCreate.as_view(), name='api_donations'),
    path('donations/<int:pk>/', DonationDetail.as_view(), name='api_donation_detail'),

    # Pedidos
    path('requests/', RequestListCreate.as_view(), name='api_requests'),
    path('requests/<int:pk>/', RequestDetail.as_view(), name='api_request_detail'),

    # Usuários (apenas admin)
    path('users/', UserList.as_view(), name='api_users'),
    path('users/<int:pk>/', UserDetail.as_view(), name='api_user_detail'),
]
