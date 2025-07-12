# apps/suggestions/views.py

from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.base import ContentFile # <-- Impor ini

from .models import Suggestion
from .serializers import SuggestionSerializer
from apps.destinations.models import Destination, DestinationImage as DestinationImageModel
from apps.common.models import Address, Contact

class SuggestionViewSet(viewsets.ModelViewSet):
    serializer_class = SuggestionSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'suggester__username', 'regency']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Suggestion.objects.all().select_related('suggester', 'category').order_by('-created_at')
        return Suggestion.objects.filter(suggester=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(suggester=self.request.user)

    def update(self, request, *args, **kwargs):
        suggestion = self.get_object()
        new_status = request.data.get('status')
        old_status = suggestion.status

        response = super().update(request, *args, **kwargs)

        if response.status_code == 200 and new_status == 'approved' and old_status != 'approved':
            self.create_destination_from_suggestion(suggestion)
            print(f"Suggestion '{suggestion.name}' disetujui, destinasi baru dibuat.")

        return response

    def create_destination_from_suggestion(self, suggestion):
        if Destination.objects.filter(name=suggestion.name).exists():
            print(f"Destinasi '{suggestion.name}' sudah ada, proses pembuatan dibatalkan.")
            return

        new_address = Address.objects.create(
            street=suggestion.street, sub_district=suggestion.sub_district,
            regency=suggestion.regency, latitude=suggestion.latitude, longitude=suggestion.longitude
        ) if suggestion.street else None

        new_contact = Contact.objects.create(
            phone_number=suggestion.phone_number, email=suggestion.email
        ) if suggestion.phone_number or suggestion.email else None
        
        price_range = ""
        if suggestion.entrance_ticket_min and suggestion.entrance_ticket_max:
            price_range = f"Rp {int(suggestion.entrance_ticket_min):,} - Rp {int(suggestion.entrance_ticket_max):,}"
        elif suggestion.entrance_ticket_min:
            price_range = f"Starting from Rp {int(suggestion.entrance_ticket_min):,}"

        destination = Destination.objects.create(
            name=suggestion.name, description=suggestion.descriptions, ticket_price_range=price_range,
            address=new_address, contact=new_contact, is_published=True
        )
        
        if suggestion.category:
            destination.categories.add(suggestion.category)
        destination.facilities.set(suggestion.facilities.all())

        # =================================================================
        # PERBAIKAN UTAMA ADA DI SINI: Cara menyalin foto yang lebih aman
        # =================================================================
        is_first_image = True
        for photo in suggestion.photos.all():
            try:
                # Buka file gambar sumber
                photo.image.open()
                # Buat objek file baru dari konten gambar sumber
                image_content = ContentFile(photo.image.read())
                photo.image.close()

                # Dapatkan nama file asli
                image_name = photo.image.name.split('/')[-1]

                # Buat objek DestinationImage baru dan simpan filenya
                new_photo = DestinationImageModel(destination=destination, is_primary=is_first_image)
                new_photo.image.save(image_name, image_content, save=True)
                
                is_first_image = False
            except Exception as e:
                # Jika ada error saat menyalin satu foto, cetak errornya dan lanjutkan
                print(f"Gagal menyalin foto {photo.image.name}: {e}")
        # =================================================================

    @action(detail=False, methods=['get'], url_path='my-suggestions')
    def my_suggestions(self, request):
        queryset = self.get_queryset().filter(suggester=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
