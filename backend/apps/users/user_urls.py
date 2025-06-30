# apps/users/urls_users.py (file baru untuk manajemen pengguna)
from django.urls import path
from .views import (
    UserListViewForAdmin, UserCreateAPIView,
)

# Anda bisa menambahkan app_name di sini jika Anda mau
app_name = 'users_management_api' # Contoh nama namespace untuk manajemen

urlpatterns = [
    path('', UserListViewForAdmin.as_view(), name='list_users'),
    path('create-admin/', UserCreateAPIView.as_view(), name='create_admin'),
]