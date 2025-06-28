# backend/apps/wishlists/serializers.py
from rest_framework import serializers
from .models import Wishlist
# Pastikan path import ini sesuai
from apps.destinations.serializers import DestinationListSerializer


class WishlistReadSerializer(serializers.ModelSerializer):
    """Serializer untuk membaca/menampilkan data wishlist dengan detail destinasi."""
    destination = DestinationListSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ['id', 'destination', 'created_at']


class WishlistWriteSerializer(serializers.ModelSerializer):
    """Serializer untuk menambah item ke wishlist (hanya perlu ID destinasi)."""
    class Meta:
        model = Wishlist
        fields = ['destination']
