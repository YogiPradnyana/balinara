# apps/common/views.py
from rest_framework import viewsets, permissions
from .models import Category, Facility
from .serializers import CategorySerializer, FacilitySerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows categories to be viewed.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    # Siapa saja bisa melihat kategori
    permission_classes = [permissions.AllowAny]
    # lookup_field = 'slug' # Jika Anda menggunakan slug untuk lookup


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows facilities to be viewed.
    """
    queryset = Facility.objects.all().order_by('name')
    serializer_class = FacilitySerializer
    # Siapa saja bisa melihat fasilitas
    permission_classes = [permissions.AllowAny]
