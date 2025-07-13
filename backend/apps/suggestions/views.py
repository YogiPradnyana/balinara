# apps/suggestions/views.py

from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.base import ContentFile

# Impor semua model yang dibutuhkan
from .models import Suggestion, TemporarySuggestionPhoto, SuggestionPhoto # Pastikan SuggestionPhoto juga diimpor
from .serializers import SuggestionSerializer, TemporarySuggestionPhotoSerializer
from apps.destinations.models import Destination, DestinationImage as DestinationImageModel
from apps.common.models import Address, Contact, Category, Facility # Pastikan Category dan Facility diimpor

class SuggestionViewSet(viewsets.ModelViewSet):
    """
    ViewSet untuk mengelola semua hal yang berhubungan dengan Suggestion.
    """
    serializer_class = SuggestionSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'suggester__username', 'regency']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        # --- PERBAIKAN KRUSIAL DI SINI: UBAH select_related('category') menjadi prefetch_related('categories') ---
        # Gunakan prefetch_related untuk Many-to-Many fields (categories, facilities, photos)
        # Gunakan select_related untuk ForeignKey (suggester)
        # Ini akan mengambil data relasi secara efisien untuk serializer
        queryset = Suggestion.objects.all().select_related('suggester').prefetch_related('categories', 'facilities', 'photos').order_by('-created_at')

        if not self.request.user.is_staff:
            # Jika bukan staff, hanya tampilkan suggestion yang dibuat oleh user tersebut
            queryset = queryset.filter(suggester=self.request.user)
        
        return queryset

    def perform_create(self, serializer):
        # Method perform_create ini akan memanggil serializer.save().
        # Karena kita sudah meng-override method create() di serializer untuk menangani
        # `suggester`, `categories`, `facilities`, dan `temp_photo_ids`,
        # tidak perlu pass `suggester` secara eksplisit di sini lagi
        # kecuali Anda memiliki alasan khusus. Cukup panggil serializer.save()
        serializer.save(suggester=self.request.user)


    def update(self, request, *args, **kwargs):
        suggestion = self.get_object()
        new_status = request.data.get('status')
        old_status = suggestion.status
        
        # Panggil method update bawaan ModelViewSet
        response = super().update(request, *args, **kwargs)
        
        # Jika update berhasil dan status berubah menjadi 'approved'
        if response.status_code == 200 and new_status == 'approved' and old_status != 'approved':
            self.create_destination_from_suggestion(suggestion)
        return response

    def create_destination_from_suggestion(self, suggestion):
        # Periksa duplikasi nama sebelum membuat Destination baru
        if Destination.objects.filter(name=suggestion.name).exists():
            print(f"Destination '{suggestion.name}' already exists. Skipping creation.")
            return

        # Buat objek Address
        new_address = None
        if suggestion.street: # Periksa apakah ada data alamat yang cukup
            new_address = Address.objects.create(
                street=suggestion.street,
                sub_district=suggestion.sub_district,
                regency=suggestion.regency,
                latitude=suggestion.latitude,
                longitude=suggestion.longitude
            )
        
        # Buat objek Contact
        new_contact = None
        if suggestion.phone_number or suggestion.email: # Periksa apakah ada data kontak
            new_contact = Contact.objects.create(
                phone=suggestion.phone_number,
                mail=suggestion.email
            )
        
        # Format rentang harga
        price_range = ""
        if suggestion.entrance_ticket_min and suggestion.entrance_ticket_max:
            price_range = f"Rp {int(suggestion.entrance_ticket_min):,} - Rp {int(suggestion.entrance_ticket_max):,}"
        elif suggestion.entrance_ticket_min:
            price_range = f"Mulai dari Rp {int(suggestion.entrance_ticket_min):,}"
        
        # Buat Destination baru
        destination = Destination.objects.create(
            name=suggestion.name,
            description=suggestion.descriptions,
            ticket_price_range=price_range,
            address=new_address,
            contact=new_contact,
            is_published=True
        )

        # --- PERBAIKAN DI SINI: Tambahkan categories ke Destination (sekarang ManyToMany) ---
        # Gunakan .set() untuk Many-to-Many
        if suggestion.categories.exists(): # Periksa apakah ada kategori yang terhubung
            destination.categories.set(suggestion.categories.all())
        
        # Tambahkan fasilitas ke Destination (ini sudah ManyToMany, logikanya sudah benar)
        destination.facilities.set(suggestion.facilities.all())

        # Salin foto dari Suggestion ke Destination
        is_first_image = True
        for photo in suggestion.photos.all():
            try:
                # Pastikan file dibuka dan dibaca dalam mode biner
                with photo.image.open('rb') as f:
                    image_content = ContentFile(f.read())
                
                image_name = photo.image.name.split('/')[-1]
                new_photo = DestinationImageModel(destination=destination, is_primary=is_first_image)
                new_photo.image.save(image_name, image_content, save=True)
                is_first_image = False
            except Exception as e:
                print(f"Gagal menyalin foto {photo.image.name}: {e}")
        
        print(f"Destination '{destination.name}' created from suggestion {suggestion.id}")

    # =================================================================
    # PASTIKAN ACTION INI ADA (ini sudah benar)
    # Ini adalah endpoint untuk upload gambar sementara.
    # =================================================================
    @action(detail=False, methods=['post'], url_path='temp-images')
    def upload_temp_image(self, request):
        serializer = TemporarySuggestionPhotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['get'], url_path='my-suggestions')
    def my_suggestions(self, request):
        # get_queryset() sudah menangani filter berdasarkan user,
        # jadi kita bisa memanggilnya langsung.
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)