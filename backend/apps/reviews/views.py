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

    def _update_destination_ratings(self, destination):
        """Fungsi helper untuk menghitung ulang dan menyimpan rating destinasi."""
        # Ambil ulang objek dari DB untuk memastikan data konsisten
        destination.refresh_from_db()

        aggregates = destination.reviews.aggregate(
            average_rating=Avg('rating'),
            total_reviews=Count('id')
        )

        destination.average_rating = aggregates['average_rating'] or 0
        destination.total_reviews = aggregates['total_reviews'] or 0
        destination.save(update_fields=['average_rating', 'total_reviews'])

    def perform_create(self, serializer):
        """Dijalankan setelah review baru berhasil divalidasi."""
        # Simpan review baru dan hubungkan dengan user yang sedang login
        review = serializer.save(user=self.request.user)

        # Panggil fungsi helper untuk langsung menghitung ulang dan memperbarui rating
        self._update_destination_ratings(review.destination)

    def perform_destroy(self, instance):
        """Dijalankan sebelum sebuah review dihapus."""
        # Simpan referensi ke destinasi sebelum review dihapus
        destination = instance.destination

        # Hapus reviewnya
        instance.delete()

        # Panggil fungsi helper untuk update rating setelah dihapus
        self._update_destination_ratings(destination)

    def list(self, request, *args, **kwargs):
        """
         Ganti metode list default untuk membuat struktur respons kustom
         DAN menerapkan semua filter yang ada.
         """

        queryset = self.filter_queryset(self.get_queryset())

        summary = {
            'total_reviews': queryset.count(),
            'average_rating': queryset.aggregate(avg=Avg('rating'))['avg'] or 0,
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

        page = self.paginate_queryset(queryset)

        if page is not None:
            reviews_serializer = self.get_serializer(page, many=True)
            paginated_response = self.get_paginated_response(
                reviews_serializer.data)

            paginated_response.data['summary'] = summary
            return paginated_response

        reviews_serializer = self.get_serializer(queryset, many=True)

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
