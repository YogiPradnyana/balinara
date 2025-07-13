# backend/apps/reviews/filters.py

import django_filters
from .models import Review


class ReviewFilter(django_filters.FilterSet):
    destination = django_filters.NumberFilter(field_name='destination_id')

    rating = django_filters.NumberFilter(
        field_name='rating', lookup_expr='exact')

    month = django_filters.NumberFilter(
        field_name='created_at', lookup_expr='month')

    user = django_filters.NumberFilter(field_name='user_id')

    class Meta:
        model = Review
        fields = ['destination', 'rating', 'month', 'user']
