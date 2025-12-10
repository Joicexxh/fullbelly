# fullbelly/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # páginas públicas (templates)
    path('', core_views.index, name='index'),
    path('register/', core_views.register_view, name='register'),
    path('login/', core_views.login_view, name='login'),
    path('logout/', core_views.logout_view, name='logout'),
    path('user/', core_views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', core_views.admin_dashboard_view, name='admin_dashboard'),

    # API (DRF)
    path('api/', include('core.urls')),

    # JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
