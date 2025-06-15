# apps/common/views.py
from rest_framework import viewsets, permissions
from .models import Category, Facility
from .serializers import CategorySerializer, FacilitySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed, created, edited or deleted.
    """
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    # Siapa saja bisa melihat kategori
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows facilities to be viewed.
    """
    queryset = Facility.objects.all().order_by('name')
    serializer_class = FacilitySerializer
    # Siapa saja bisa melihat fasilitas
    permission_classes = [permissions.AllowAny]
