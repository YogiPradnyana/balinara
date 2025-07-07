# backend/apps/reviews/filters.py

import django_filters
from .models import Review


class ReviewFilter(django_filters.FilterSet):
    # Filter ini akan menerima ?rating=5, ?rating=4, dst.
    rating = django_filters.NumberFilter(
        field_name='rating', lookup_expr='exact')

    month = django_filters.NumberFilter(
        field_name='created_at', lookup_expr='month')

    class Meta:
        model = Review
        fields = ['rating', 'month']
