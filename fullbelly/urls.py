from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.http import JsonResponse

# Rota de teste para a home / raiz da API
def home(request):
    return JsonResponse({
        "message": "API Full Belly funcionando!",
        "status": "ok",
        "routes": [
            "/api/",
            "/api/token/",
            "/api/token/refresh/"
        ]
    })

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Home / raiz
    path('', home, name='home'),

    # API (DRF)
    path('api/', include('core.urls')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

