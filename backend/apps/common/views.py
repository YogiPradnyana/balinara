# apps/common/views.py
from rest_framework import viewsets, permissions
from .models import Category, Facility
from .serializers import CategorySerializer, FacilitySerializer
# Pastikan SearchFilter diimpor
from rest_framework.filters import SearchFilter, OrderingFilter
# Jika Anda juga pakai filter lain
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed, created, edited or deleted.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Siapa saja bisa melihat kategori
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend, SearchFilter,
                       OrderingFilter]
    search_fields = ['name', 'slug']


class FacilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows facilities to be viewed, created, edited or deleted.
    """
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    # Siapa saja bisa melihat fasilitas
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    filter_backends = [DjangoFilterBackend, SearchFilter,
                       OrderingFilter]
    search_fields = ['name', 'slug']
