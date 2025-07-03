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

from .models import Destination, DestinationImage, TemporaryImage
from .serializers import (
    DestinationListSerializer,
    DestinationDetailCRUDSerializer,
    DestinationImageSerializer,
    TemporaryImageSerializer
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
    ordering = ['-id', 'name']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return DestinationListSerializer
        # Untuk retrieve, create, update, partial_update, destroy, gunakan serializer CRUD
        return DestinationDetailCRUDSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.filter(is_deleted=False)

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

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()

    @action(detail=True, methods=['post'], url_path='toggle-publish')
    def toggle_publish_status(self, request, slug=None):
        """
        Endpoint untuk mengubah status is_published dengan satu kali klik.
        Contoh request: POST /api/destinations/{slug}/toggle-publish/
        """
        try:
            destination = self.get_object()
            # Balikkan nilainya: jika True menjadi False, jika False menjadi True
            destination.is_published = not destination.is_published
            destination.save(update_fields=['is_published'])

            # Kembalikan data terbaru
            serializer = self.get_serializer(destination)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser],
            url_path='images/(?P<image_pk>[0-9]+)/set-primary')
    def set_primary_image(self, request, slug=None, image_pk=None):
        """
        Action untuk menetapkan sebuah gambar sebagai primary.
        """
        destination = self.get_object()  # Memastikan destinasi ada
        try:
            # Cari gambar yang dimaksud dan pastikan gambar itu milik destinasi ini
            image_to_set = DestinationImage.objects.get(
                id=image_pk, destination=destination)

            # Set sebagai primary dan simpan.
            # Logika di model DestinationImage.save() akan otomatis menangani
            # unset primary pada gambar lainnya.
            image_to_set.is_primary = True
            image_to_set.save()

            # Kembalikan data destinasi yang sudah terupdate agar frontend bisa sinkronisasi
            serializer = self.get_serializer(destination)
            return Response(serializer.data)

        except DestinationImage.DoesNotExist:
            return Response({'error': 'Image not found for this destination.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Action untuk upload gambar
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser],
            parser_classes=[MultiPartParser, FormParser], url_path='images/upload')
    def upload_image(self, request, slug=None):
        destination = self.get_object()
        images = request.FILES.getlist('images')

        if not images:
            return Response({'detail': 'No image files were provided.'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_images_data = []
        errors = []

        # Ambil data teks non-file sekali saja (jika ada)
        alt_text_base = request.data.get(
            'alt_text', f"Image for {destination.name}")

        for image_file in images:
            # --- INI LOGIKA BARU YANG PENTING ---
            # Buat paket data LENGKAP untuk setiap gambar
            data_for_serializer = {
                'alt_text': alt_text_base,
                'image': image_file  # <-- Masukkan objek file ke dalam data
            }

            serializer = DestinationImageSerializer(
                data=data_for_serializer, context={'request': request})

            # Sekarang is_valid() akan berhasil karena 'image' sudah ada di dalam data
            if serializer.is_valid():
                try:
                    # 'image' sudah ada di validated_data, kita hanya perlu tambahkan 'destination'
                    serializer.save(destination=destination)
                    uploaded_images_data.append(serializer.data)
                except Exception as e:
                    errors.append({image_file.name: str(e)})
            else:
                errors.append({image_file.name: serializer.errors})

        if errors:
            return Response({
                'status': 'Completed with errors',
                'errors': errors,
                'successful_uploads': uploaded_images_data
            }, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'status': 'All images uploaded successfully',
            'uploaded_images': uploaded_images_data
        }, status=status.HTTP_201_CREATED)

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


class TemporaryImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint untuk mengunggah dan menghapus gambar sementara.
    - POST /api/destinations/temp-images/ : unggah gambar baru
    - DELETE /api/destinations/temp-images/{id}/ : hapus gambar sementara
    """
    queryset = TemporaryImage.objects.all()
    serializer_class = TemporaryImageSerializer
    # Hanya admin yang bisa upload
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    http_method_names = ['post', 'delete', 'head', 'options']

    def create(self, request, *args, **kwargs):
        """
        Hanya menangani satu file per request. Ini adalah implementasi standar
        yang seharusnya tidak menyebabkan duplikasi.
        """
        image_file = request.FILES.get('image')
        if not image_file:
            return Response(
                {'detail': 'No image file provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Buat data untuk serializer
        data = {'image': image_file}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        # perform_create akan memanggil serializer.save() yang menyimpan objek
        # dan file ke storage HANYA SATU KALI.
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
