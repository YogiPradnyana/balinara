# apps/destinations/filters.py
import django_filters
# Impor model yang relevan untuk filter
from apps.common.models import Category, Facility
from .models import Destination


class DestinationFilter(django_filters.FilterSet):
    # Contoh filter:
    # Filter berdasarkan nama kategori (case-insensitive contains)
    category_name = django_filters.CharFilter(
        field_name='category__name', lookup_expr='icontains')
    # Filter berdasarkan slug kategori (exact match)
    category_slug = django_filters.CharFilter(
        field_name='category__slug', lookup_expr='exact')
    # Filter berdasarkan nama fasilitas (case-insensitive contains)
    facility_name = django_filters.CharFilter(
        field_name='facilities__name', lookup_expr='icontains')
    # Filter berdasarkan ID fasilitas
    facility_id = django_filters.NumberFilter(
        field_name='facilities__id', lookup_expr='exact')

    # Filter berdasarkan rentang average_rating
    min_rating = django_filters.NumberFilter(
        field_name="average_rating", lookup_expr='gte')
    max_rating = django_filters.NumberFilter(
        field_name="average_rating", lookup_expr='lte')

    # Filter berdasarkan regency di alamat
    regency = django_filters.CharFilter(
        field_name='address__regency', lookup_expr='icontains')

    class Meta:
        model = Destination
        # Daftar field yang ingin Anda filter secara sederhana (exact match defaultnya)
        # atau Anda bisa mendefinisikan setiap filter secara eksplisit seperti di atas
        # untuk kontrol lookup_expr yang lebih baik.
        fields = {
            'name': ['icontains'],  # Contoh: ?name__icontains=Kuta
            'is_published': ['exact'],  # ?is_published=true
            # 'category': ['exact'], # Ini akan filter berdasarkan ID kategori
            # 'facilities': ['exact'], # Ini akan filter berdasarkan ID fasilitas
        }
        # Jika Anda sudah mendefinisikan filter secara eksplisit (seperti category_slug),
        # Anda tidak perlu menambahkannya lagi di Meta.fields kecuali ingin perilaku default tambahan.
