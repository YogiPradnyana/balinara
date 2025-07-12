from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from .models import Review, TemporaryReviewImage
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count
from .serializers import ReviewSerializer, TemporaryReviewImageSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import ReviewFilter


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('user')
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ReviewFilter
    search_fields = ['comment', 'user__username']

    def perform_create(self, serializer):
        # Set user secara otomatis berdasarkan user yang sedang login
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """
         Ganti metode list default untuk membuat struktur respons kustom
         DAN menerapkan semua filter yang ada.
         """
        queryset = self.get_queryset()

        filtered_queryset = self.filter_queryset(queryset)

        summary = {
            'total_reviews': filtered_queryset.count(),
            'average_rating': filtered_queryset.aggregate(avg=Avg('rating'))['avg'] or 0,
            'rating_distribution': []
        }

        distribution = queryset.values('rating').annotate(
            count=Count('rating')).order_by('-rating')
        total_for_percentage = queryset.count()
        distribution_map = {item['rating']: item['count']
                            for item in distribution}

        for i in range(5, 0, -1):
            count = distribution_map.get(i, 0)
            percentage = (count / total_for_percentage *
                          100) if total_for_percentage > 0 else 0
            summary['rating_distribution'].append({
                'rating': i,
                'count': count,
                'percentage': round(percentage)
            })

        page = self.paginate_queryset(filtered_queryset)

        if page is not None:
            reviews_serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(
                reviews_serializer.data)

            paginated_response.data['summary'] = summary
            return paginated_response

        reviews_serializer = self.get_serializer(filtered_queryset, many=True)

        custom_data = {
            'summary': summary,
            'reviews': reviews_serializer.data
        }

        return Response(custom_data)


class TemporaryReviewImageViewSet(viewsets.ModelViewSet):
    queryset = TemporaryReviewImage.objects.all()
    serializer_class = TemporaryReviewImageSerializer
    # Hanya user login yang bisa upload
    permission_classes = [permissions.AllowAny]
    http_method_names = ['post', 'delete']
