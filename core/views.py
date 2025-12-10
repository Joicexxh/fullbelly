from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Donation, Request
from .serializers import DonationSerializer, RequestSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

# ---------- Templates (páginas públicas e dashboards) ----------
def index(request):
    donations = Donation.objects.filter(status='available').order_by('-created_at')[:10]
    return render(request, 'index.html', {'donations': donations})

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            messages.success(request, 'Cadastro realizado.')
            return redirect('user_dashboard')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Bem-vinda(o)!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Credenciais inválidas.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def user_dashboard(request):
    user = request.user
    donations = Donation.objects.filter(donor=user).order_by('-created_at')
    requests_ = Request.objects.filter(requester=user).order_by('-created_at')
    return render(request, 'user_dashboard.html', {'donations': donations, 'requests': requests_, 'user': user})

def is_admin(user):
    return user.is_staff

@user_passes_test(is_admin)
def admin_dashboard_view(request):
    users = User.objects.all().order_by('-date_joined')
    donations = Donation.objects.all().order_by('-created_at')
    requests_ = Request.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard.html', {'users': users, 'donations': donations, 'requests': requests_})

# ---------- API views (DRF generic) ----------
class DonationListCreate(generics.ListCreateAPIView):
    queryset = Donation.objects.all().order_by('-created_at')
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

class RequestListCreate(generics.ListCreateAPIView):
    queryset = Request.objects.all().order_by('-created_at')
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

# Registro via API simples (opcional)
class RegisterAPI(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        if User.objects.filter(username=username).exists():
            return Response({'error':'username_exists'}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response(UserSerializer(user).data)
