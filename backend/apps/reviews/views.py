from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Review, TemporaryReviewImage
from django.db.models import Avg, Count
from .serializers import ReviewSerializer, TemporaryReviewImageSerializer
from .permissions import IsOwnerOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().select_related('user')
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Filter review berdasarkan destinasi jika parameter destination_id ada di URL
        destination_id = self.request.query_params.get('destination_id')
        if destination_id:
            return self.queryset.filter(destination_id=destination_id)
        return self.queryset.none()  # Jangan tampilkan semua review jika tidak ada filter

    def perform_create(self, serializer):
        # Set user secara otomatis berdasarkan user yang sedang login
        serializer.save(user=self.request.user)

    def list(self, request, *args, **kwargs):
        """
        Ganti metode list default untuk membuat struktur respons kustom.
        """
        # 1. Dapatkan queryset yang sudah difilter berdasarkan destinasi
        queryset = self.get_queryset()

        # 2. Hitung data untuk summary
        summary = {
            'total_reviews': queryset.count(),
            'average_rating': queryset.aggregate(avg=Avg('rating'))['avg'] or 0,
            'rating_distribution': []
        }

        # Hitung distribusi rating (bintang 1 sampai 5)
        distribution = queryset.values('rating').annotate(
            count=Count('rating')).order_by('-rating')
        distribution_map = {item['rating']: item['count']
                            for item in distribution}

        for i in range(5, 0, -1):
            count = distribution_map.get(i, 0)
            percentage = (
                count / summary['total_reviews'] * 100) if summary['total_reviews'] > 0 else 0
            summary['rating_distribution'].append({
                'rating': i,
                'count': count,
                'percentage': round(percentage)
            })

        # 3. Ambil review-nya (tidak perlu paginasi untuk daftar pendek ini)
        reviews_serializer = self.get_serializer(queryset, many=True)

        # 4. Gabungkan semuanya dalam satu respons
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
