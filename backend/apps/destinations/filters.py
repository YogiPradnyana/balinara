import django_filters
from .models import Destination


class CommaSeparatedCharFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class DestinationFilter(django_filters.FilterSet):

    # Untuk filter kategori berdasarkan slug. Sekarang bisa menerima ?category_slug=pura,pantai
    category_slug = CommaSeparatedCharFilter(
        field_name='category__slug', lookup_expr='in')

    # Untuk filter kabupaten. Sekarang bisa menerima ?regency=badung,gianyar
    regency = CommaSeparatedCharFilter(
        field_name='address__regency', lookup_expr='in')

    # Filter berdasarkan nama kategori (case-insensitive contains)
    category_name = django_filters.CharFilter(
        field_name='category__name', lookup_expr='icontains')

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
        fields = {
            'name': ['icontains'],  # Contoh: ?name__icontains=Kuta
            'is_published': ['exact'],  # ?is_published=true
            # 'category': ['exact'], # Ini akan filter berdasarkan ID kategori
            # 'facilities': ['exact'], # Ini akan filter berdasarkan ID fasilitas
        }
