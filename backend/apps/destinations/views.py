# apps/destinations/views.py
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
# Untuk menangani berbagai tipe request
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
# Untuk filtering berdasarkan field
from django_filters.rest_framework import DjangoFilterBackend
# Untuk pencarian dan pengurutan
from rest_framework.filters import SearchFilter, OrderingFilter

from .models import Destination, DestinationImage
from .serializers import (
    DestinationListSerializer,
    DestinationDetailSerializer,
    DestinationImageSerializer
)
# Impor jika perlu untuk filter atau validasi
from apps.common.models import Category, Facility
# Impor jika perlu untuk endpoint terpisah
from apps.common.serializers import CategorySerializer, FacilitySerializer

# === ViewSet untuk Destinasi ===


class DestinationViewSet(viewsets.ModelViewSet):
    """
    API endpoint yang memungkinkan destinasi untuk dilihat, dibuat, diupdate, atau dihapus.
    - List: GET /api/destinations/ (dengan filter, search, ordering)
    - Create: POST /api/destinations/ (membutuhkan autentikasi admin)
    - Retrieve: GET /api/destinations/{id_atau_slug}/
    - Update: PUT /api/destinations/{id_atau_slug}/ (membutuhkan autentikasi admin)
    - Partial Update: PATCH /api/destinations/{id_atau_slug}/ (membutuhkan autentikasi admin)
    - Destroy: DELETE /api/destinations/{id_atau_slug}/ (membutuhkan autentikasi admin)
    - Upload Image: POST /api/destinations/{id_atau_slug}/upload_image/
    - Delete Image: DELETE /api/destinations/{id_atau_slug}/delete_image/{image_pk}/
    """
    # Queryset default, hanya tampilkan yang sudah dipublikasi untuk non-admin
    # Admin akan melihat semua di Django Admin interface
    queryset = Destination.objects.filter(is_published=True)\
        .select_related('category', 'address', 'contact')\
        .prefetch_related('facilities', 'images')  # Optimasi query

    parser_classes = [MultiPartParser, FormParser,
                      JSONParser]  # Izinkan berbagai tipe input

    # Konfigurasi untuk filtering, searching, dan ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = {  # Filter yang lebih spesifik
        'category__slug': ['exact'],  # ?category__slug=nama-slug-kategori
        # ?address__regency=Gianyar
        'address__regency': ['iexact', 'icontains'],
        # ?facilities__id=1 (filter by facility ID)
        'facilities__id': ['exact'],
        'average_rating': ['gte', 'lte', 'exact'],  # ?average_rating__gte=4.0
    }
    search_fields = [  # Field yang bisa dicari menggunakan ?search=keyword
        'name',
        'description',
        'category__name',
        'address__street',
        'address__sub_district',
        'address__regency',
        'facilities__name'
    ]
    ordering_fields = ['name', 'average_rating', 'total_reviews',
                       'created_at', 'updated_at']  # Field untuk ?ordering=
    ordering = ['-average_rating', 'name']  # Default ordering

    lookup_field = 'slug'  # Menggunakan slug sebagai lookup selain pk (ID)
    # Pastikan slug unik. Jika tidak, gunakan 'pk' saja.

    def get_serializer_class(self):
        if self.action == 'list':
            return DestinationListSerializer  # Serializer ringkas untuk daftar
        # Untuk retrieve, create, update, partial_update, destroy, gunakan serializer detail
        return DestinationDetailSerializer

    def get_permissions(self):
        """
        Mengatur permission berdasarkan aksi.
        - Siapa saja bisa melihat daftar (list) dan detail (retrieve).
        - Hanya admin (atau user terautentikasi dengan logic tambahan) yang bisa membuat,
          mengupdate, atau menghapus destinasi.
        """
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [permissions.AllowAny]
        # create, update, partial_update, destroy, dan custom actions (upload_image, delete_image)
        else:
            self.permission_classes = [permissions.IsAdminUser]  # Hanya admin
            # Atau, jika user biasa bisa membuat/mengedit destinasi mereka sendiri:
            # self.permission_classes = [permissions.IsAuthenticated]
            # dan Anda perlu menambahkan logika untuk cek ownership di perform_update/perform_destroy
        return super().get_permissions()

    def perform_create(self, serializer):
        # Jika Anda ingin set 'created_by' secara otomatis saat admin membuat destinasi
        # if self.request.user.is_authenticated and self.request.user.is_staff:
        #     serializer.save(created_by=self.request.user)
        # else:
        serializer.save()  # Simpan data destinasi

    def perform_update(self, serializer):
        # Jika Anda ingin set 'last_updated_by'
        # if self.request.user.is_authenticated and self.request.user.is_staff:
        #     serializer.save(last_updated_by=self.request.user)
        # else:
        serializer.save()

    # Action kustom untuk mengunggah gambar ke destinasi yang sudah ada
    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser],
            parser_classes=[MultiPartParser, FormParser], url_path='upload-image')
    # Menggunakan slug karena lookup_field='slug'
    def upload_image(self, request, slug=None):
        destination = self.get_object()  # Mendapatkan instance Destination
        # 'image' adalah nama field yang diharapkan dari FormData
        # 'alt_text' dan 'is_primary' bisa dikirim juga
        serializer_context = {'request': request}  # Penting untuk image_url
        image_serializer = DestinationImageSerializer(
            data=request.data, context=serializer_context)

        if image_serializer.is_valid():
            # Pastikan ada file gambar yang diupload
            if 'image' not in request.FILES:
                return Response({'error': 'No image file provided in the "image" field.'}, status=status.HTTP_400_BAD_REQUEST)

            # Set relasi destination
            image_serializer.save(destination=destination)
            return Response(image_serializer.data, status=status.HTTP_201_CREATED)
        return Response(image_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Action kustom untuk menghapus gambar dari destinasi
    @action(detail=True, methods=['delete'], permission_classes=[permissions.IsAdminUser],
            # (?P<image_pk>[0-9]+) menangkap ID gambar
            url_path='delete-image/(?P<image_pk>[0-9]+)')
    def delete_image(self, request, slug=None, image_pk=None):
        destination = self.get_object()
        try:
            image_instance = DestinationImage.objects.get(
                id=image_pk, destination=destination)
            # Ini akan memanggil metode delete kustom di model DestinationImage
            image_instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except DestinationImage.DoesNotExist:
            return Response({'error': 'Image not found for this destination.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
