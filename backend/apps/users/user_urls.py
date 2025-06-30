# apps/users/urls_users.py (file baru untuk manajemen pengguna)
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserCreateAPIView, UserManagementViewSet
)

router = DefaultRouter()

router.register(r'', UserManagementViewSet, basename='admin-user-management')

# Anda bisa menambahkan app_name di sini jika Anda mau
app_name = 'users_management_api' # Contoh nama namespace untuk manajemen

urlpatterns = [
    path('create-admin/', UserCreateAPIView.as_view(), name='create_admin'),
    path('', include(router.urls)),
    
]