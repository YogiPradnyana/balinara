# apps/suggestions/views.py

from rest_framework import viewsets, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Suggestion
from .serializers import SuggestionSerializer

class SuggestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk mengelola Suggestions.
    - User yang login bisa membuat suggestion baru (POST).
    - User yang login bisa melihat daftar suggestion miliknya (GET /my-suggestions/).
    - Admin bisa melihat dan mengelola semua suggestion.
    """
    serializer_class = SuggestionSerializer
    parser_classes = (MultiPartParser, FormParser)
    
    # 1. Mengamankan endpoint: Hanya user yang sudah login yang bisa mengakses
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Fungsi ini mengatur data apa yang ditampilkan.
        User biasa hanya akan melihat daftar saran miliknya sendiri.
        """
        # Jika user adalah staff/admin, tampilkan semua suggestion
        if self.request.user.is_staff:
            return Suggestion.objects.all().order_by('-created_at')
        # Jika user biasa, tampilkan hanya suggestion miliknya
        return Suggestion.objects.filter(suggester=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        """
        2. Fungsi ini otomatis mengisi field 'suggester' dengan 
           user yang sedang login saat data baru dibuat.
        """
        serializer.save(suggester=self.request.user)

    # 3. Menambahkan endpoint baru: /api/suggestions/my-suggestions/
    @action(detail=False, methods=['get'], url_path='my-suggestions')
    def my_suggestions(self, request):
        """
        Endpoint kustom untuk secara eksplisit mengambil daftar saran 
        milik user yang sedang login.
        """
        # queryset sudah otomatis terfilter oleh get_queryset(), jadi kita bisa pakai ulang
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)