# backend/apps/wishlists/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Wishlist
from .serializers import WishlistReadSerializer, WishlistWriteSerializer


class WishlistListCreateView(generics.ListCreateAPIView):
    """
    GET: Tampilkan semua item di wishlist pengguna yang sedang login.
    POST: Tambahkan item baru ke wishlist pengguna yang sedang login.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        # Gunakan serializer yang berbeda untuk membaca (GET) dan menulis (POST)
        if self.request.method == 'POST':
            return WishlistWriteSerializer
        return WishlistReadSerializer

    def get_queryset(self):
        # PENTING: Filter queryset agar hanya menampilkan item milik user yang sedang request
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # PENTING: Set user secara otomatis berdasarkan user yang sedang login
        serializer.save(user=self.request.user)


class WishlistDestroyView(generics.DestroyAPIView):
    """
    DELETE: Hapus item dari wishlist berdasarkan ID destinasi.
    """
    permission_classes = [permissions.IsAuthenticated]
    queryset = Wishlist.objects.all()

    def get_object(self):
        # Dapatkan objek Wishlist berdasarkan user yang login DAN ID destinasi dari URL
        return generics.get_object_or_404(
            self.get_queryset(),
            user=self.request.user,
            destination_id=self.kwargs['destination_id']
        )
