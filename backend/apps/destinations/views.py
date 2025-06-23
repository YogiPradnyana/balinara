# apps/destinations/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
# Untuk menangani berbagai tipe request
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
# Untuk filtering berdasarkan field
from django_filters.rest_framework import DjangoFilterBackend
# Untuk pencarian dan pengurutan
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import DestinationFilter

from .models import Destination, DestinationImage
from .serializers import (
    DestinationListSerializer,
    DestinationDetailCRUDSerializer,
    DestinationImageSerializer
)
# Impor jika perlu untuk filter atau validasi
from apps.common.models import Category, Facility
# Impor jika perlu untuk endpoint terpisah
from apps.common.serializers import CategorySerializer, FacilitySerializer

# === ViewSet untuk Destinasi ===


class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all().select_related(  # Ambil semua untuk admin, filter is_published di get_queryset
        'address', 'contact'
        # Tambahkan reviews jika sudah ada modelnya
    ).prefetch_related('facilities', 'images', 'categories'  # 'reviews'
                       )
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # Atau filterset_fields jika belum ada DestinationFilter
    filterset_class = DestinationFilter
    search_fields = [
        'name', 'description', 'categories__name',
        'address__regency', 'facilities__name'
    ]
    ordering_fields = ['name', 'average_rating', 'created_at']
    ordering = ['-average_rating', 'name']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return DestinationListSerializer
        # Untuk retrieve, create, update, partial_update, destroy, gunakan serializer CRUD
        return DestinationDetailCRUDSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Jika pengguna bukan staf (admin), hanya tampilkan yang is_published=True
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        else:  # create, update, partial_update, destroy, dan custom actions
            # Hanya admin yang bisa CUD
            self.permission_classes = [permissions.IsAdminUser]
        return super().get_permissions()

    def perform_create(self, serializer):
        # Logika tambahan saat create, misal set created_by jika ada fieldnya
        # serializer.save(created_by=self.request.user)
        serializer.save()

    def perform_update(self, serializer):
        # Logika tambahan saat update, misal set last_updated_by
        # serializer.save(last_updated_by=self.request.user)
        serializer.save()

    # Action untuk upload gambar
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser],
            parser_classes=[MultiPartParser, FormParser], url_path='images/upload')
    def upload_image(self, request, slug=None):
        destination = self.get_object()
        # Kirim destination ke context jika perlu
        serializer_context = {'request': request, 'destination': destination}

        # Kita bisa menerima satu atau banyak file gambar di sini
        # Jika hanya satu: request.FILES.get('image')
        # Jika banyak: request.FILES.getlist('images') -> frontend harus kirim dengan nama 'images'
        # Untuk contoh, kita asumsikan satu gambar per request ke action ini
        # Frontend akan mengirim FormData dengan field 'image', 'alt_text' (opsional), 'is_primary' (opsional)

        image_data = request.data.copy()  # Salin request data
        # Tambahkan pk destinasi secara manual jika serializer butuh
        image_data['destination'] = destination.pk
        # atau biarkan serializer.save(destination=destination)

        image_serializer = DestinationImageSerializer(
            data=image_data, context=serializer_context)

        if image_serializer.is_valid():
            if 'image' not in request.FILES:  # Pastikan file benar-benar ada di FILES
                return Response({'image': ['No image file provided.']}, status=status.HTTP_400_BAD_REQUEST)

            # Explicitly set destination
            image_serializer.save(destination=destination)
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Action untuk list gambar suatu destinasi (sebenarnya sudah ada di 'images' pada DestinationDetailCRUDSerializer)
    # Tapi ini bisa berguna jika ingin endpoint khusus gambar
    @action(detail=True, methods=['get'], permission_classes=[permissions.AllowAny], url_path='images')
    def list_images(self, request, slug=None):
        destination = self.get_object()
        # Menggunakan related_name dari DestinationImage
        images = destination.images.all()
        serializer_context = {'request': request}
        serializer = DestinationImageSerializer(
            images, many=True, context=serializer_context)
        return Response(serializer.data)

    # Action untuk menghapus gambar destinasi
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAdminUser],
            url_path='images/(?P<image_pk>[0-9]+)/delete')
    def delete_image(self, request, slug=None, image_pk=None):
        # Tidak terpakai langsung tapi baik untuk validasi awal
        destination = self.get_object()
        try:
            image_instance = DestinationImage.objects.get(
                id=image_pk, destination__slug=slug)  # Pastikan gambar milik destinasi ini
            # Ini akan memanggil metode delete kustom di model DestinationImage
            image_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DestinationImage.DoesNotExist:
            return Response({'error': 'Image not found for this destination.'}, status=status.HTTP_404_NOT_FOUND)


# === ViewSet untuk Kategori (Read-Only) ===
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint untuk melihat daftar kategori destinasi.
    - List: GET /api/categories/
    - Retrieve: GET /api/categories/{id_atau_slug}/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # Siapa saja bisa melihat kategori
    permission_classes = [permissions.AllowAny]
    # Opsional: bisa diakses via slug (jika slug unik dan ada di model Category)
    lookup_field = 'slug'


# === ViewSet untuk Fasilitas (Read-Only) ===
class FacilityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint untuk melihat daftar fasilitas yang tersedia.
    - List: GET /api/facilities/
    - Retrieve: GET /api/facilities/{id}/
    """
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    # Siapa saja bisa melihat fasilitas
    permission_classes = [permissions.AllowAny]
