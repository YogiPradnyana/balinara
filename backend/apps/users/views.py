# apps/users/views.py
from django.contrib.auth import login, logout
from rest_framework import generics, status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from .serializers import UserCreateSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from .models import User
from .permissions import CanEditOnlyNonSuperusersOrSelf, CanSetPasswordOnlyForNonSuperusersOrSelf
from django.contrib.auth import get_user_model # <-- Tambahkan ini
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer,
    UserProfileUpdateSerializer, ChangePasswordSerializer, AdminUserUpdateSerializer,  AdminSetPasswordSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key,
            "message": "User registered successfully!"
        }, status=status.HTTP_201_CREATED)


class UserLoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserDetailSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key,
            "message": "Login successful."
        }, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserProfileUpdateSerializer
        return UserDetailSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  # Untuk PATCH request
        instance = self.get_object()  # Dapatkan instance user yang akan diupdate

        # Gunakan UserProfileUpdateSerializer untuk validasi dan melakukan update
        update_serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        update_serializer.is_valid(raise_exception=True)
        self.perform_update(update_serializer)  # Melakukan save ke database

        # Jika ada prefetch_related, Django mungkin perlu invalidasi cache-nya
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        # Setelah update berhasil, serialisasi ulang instance user yang sudah terupdate
        # menggunakan UserDetailSerializer agar semua field (termasuk email) ikut dalam respons
        # Kita perlu menyediakan konteks request ke UserDetailSerializer agar get_image_url berfungsi
        detail_serializer_context = self.get_serializer_context()
        detail_serializer = UserDetailSerializer(
            instance, context=detail_serializer_context)

        return Response(detail_serializer.data, status=status.HTTP_200_OK)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserPagination(PageNumberPagination):
    page_size = 10 # Admin mungkin ingin melihat lebih banyak data per halaman
    page_size_query_param = 'page_size'
    max_page_size = 200


class UserManagementViewSet(viewsets.ModelViewSet): # Menggunakan ModelViewSet
    """
    ViewSet ini menangani operasi CRUD untuk manajemen pengguna oleh Admin.
    """
    queryset = User.objects.all().order_by('email')
    permission_classes = [permissions.IsAdminUser]
    pagination_class = AdminUserPagination

    def get_serializer_class(self):
        """
        Mengembalikan serializer class yang berbeda berdasarkan aksi (action).
        """
        if self.action in ['list', 'retrieve']:
            return UserDetailSerializer
        elif self.action in ['update', 'partial_update']:
            return AdminUserUpdateSerializer
        # Jika Anda ingin create juga di ViewSet ini (bukan hanya via create-admin/), bisa tambahkan:
        # elif self.action == 'create':
        #     return UserCreateSerializer
        return super().get_serializer_class()

    def get_serializer_context(self):
        return {'request': self.request}

    # Metode `list` dengan debugging prints (opsional, bisa dihapus)
    def list(self, request, *args, **kwargs):
        print("--- 1. SERVER: Menerima permintaan GET untuk daftar pengguna ---")
        queryset = self.filter_queryset(self.get_queryset())
        print(f"--- 2. SERVER: Query ke database berhasil, ditemukan {queryset.count()} total pengguna ---")

        page = self.paginate_queryset(queryset)
        if page is not None:
            print(f"--- 3. SERVER: Paginasi berhasil, akan memproses {len(page)} pengguna untuk halaman ini ---")
            serializer = self.get_serializer(page, many=True)
            print("--- 4. SERVER: MEMULAI PROSES SERIALISASI (mengubah data ke JSON) ---")
            serialized_data = serializer.data
            print("--- 5. SERVER: PROSES SERIALISASI BERHASIL! ---")
            return self.get_paginated_response(serialized_data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class UserCreateAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny] 


class AdminSetUserPasswordView(generics.GenericAPIView): # <-- UBAH DI SINI
    queryset = User.objects.all()
    serializer_class = AdminSetPasswordSerializer
    permission_classes = [CanSetPasswordOnlyForNonSuperusersOrSelf]
    lookup_field = 'pk'

    def get_object(self):
        # Mengambil objek user berdasarkan PK dari URL
        return self.queryset.get(pk=self.kwargs[self.lookup_field])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.get_object() # Penting: Meneruskan objek user ke serializer
        return context

    # KOREKSI: Menambahkan metode post() secara eksplisit
    def post(self, request, *args, **kwargs): # <-- TAMBAHKAN METODE POST INI
        self.object = self.get_object() # Dapatkan objek user yang akan diubah password-nya

        serializer = self.get_serializer(data=request.data, context={'user': self.object})
        serializer.is_valid(raise_exception=True)
        serializer.save() # Memanggil save di serializer

        return Response({"message": "Password updated successfully by admin."}, status=status.HTTP_200_OK)
