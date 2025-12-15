from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Donation, Request
from .serializers import DonationSerializer, RequestSerializer, UserSerializer

# ---------- API Endpoints ----------

# Index / lista últimas 10 doações disponíveis
@api_view(['GET'])
def index(request):
    donations = Donation.objects.filter(status='available').order_by('-created_at')[:10]
    serializer = DonationSerializer(donations, many=True)
    return Response({"donations": serializer.data})


# Registro de usuário
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if User.objects.filter(username=username).exists():
        return Response({'error':'username_exists'}, status=400)
    elif User.objects.filter(email=email).exists():
        return Response({'error':'email_exists'}, status=400)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    return Response(UserSerializer(user).data)


# ---------- Doações ----------
class DonationListCreate(generics.ListCreateAPIView):
    queryset = Donation.objects.all().order_by('-created_at')
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)


class DonationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(donor=self.request.user)


# ---------- Pedidos ----------
class RequestListCreate(generics.ListCreateAPIView):
    queryset = Request.objects.all().order_by('-created_at')
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)


class RequestDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(requester=self.request.user)


# ---------- Usuários ----------
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Apenas admins


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Apenas admins
