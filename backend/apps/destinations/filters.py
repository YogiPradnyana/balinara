# backend/apps/destinations/filters.py
import django_filters
from .models import Destination

# Filter kustom untuk menerima beberapa nilai yang dipisahkan koma


class CommaSeparatedCharFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class DestinationFilter(django_filters.FilterSet):
    # ==================== AWAL MODIFIKASI ====================
    # Gunakan nama yang lebih pendek dan jelas untuk parameter URL
    # Backend akan mencari 'category' di URL, contoh: ?category=pura,pantai
    category = CommaSeparatedCharFilter(
        field_name='categories__slug', lookup_expr='in'
    )

    # Backend akan mencari 'regency' di URL, contoh: ?regency=badung,gianyar
    regency = CommaSeparatedCharFilter(
        field_name='address__regency', lookup_expr='in'
    )

    # Hapus duplikasi 'regency' dan filter lain yang tidak terpakai
    # agar tidak membingungkan.
    # Filter 'min_rating' sudah benar.
    min_rating = django_filters.NumberFilter(
        field_name="average_rating", lookup_expr='gte'
    )
    # ==================== AKHIR MODIFIKASI ===================

    class Meta:
        model = Destination
        # Kita tidak perlu 'fields' ini karena kita sudah mendefinisikan
        # filter secara eksplisit di atas.
        fields = []
