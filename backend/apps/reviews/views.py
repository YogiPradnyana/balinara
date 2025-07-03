from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer
from .permissions import IsOwnerOrReadOnly  # Kita perlu buat permission ini


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
