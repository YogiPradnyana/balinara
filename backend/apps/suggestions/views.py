# apps/suggestions/views.py

from rest_framework import viewsets, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.base import ContentFile

# Impor semua model yang dibutuhkan
from .models import Suggestion, TemporarySuggestionPhoto
from .serializers import SuggestionSerializer, TemporarySuggestionPhotoSerializer
from apps.destinations.models import Destination, DestinationImage as DestinationImageModel
from apps.common.models import Address, Contact

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
        return response

    def create_destination_from_suggestion(self, suggestion):
        if Destination.objects.filter(name=suggestion.name).exists():
            return
        new_address = Address.objects.create(
            street=suggestion.street, sub_district=suggestion.sub_district,
            regency=suggestion.regency, latitude=suggestion.latitude, longitude=suggestion.longitude
        ) if suggestion.street else None
        new_contact = Contact.objects.create(
            phone=suggestion.phone_number,
            mail=suggestion.email
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
        is_first_image = True
        for photo in suggestion.photos.all():
            try:
                photo.image.open()
                image_content = ContentFile(photo.image.read())
                photo.image.close()
                image_name = photo.image.name.split('/')[-1]
                new_photo = DestinationImageModel(destination=destination, is_primary=is_first_image)
                new_photo.image.save(image_name, image_content, save=True)
                is_first_image = False
            except Exception as e:
                print(f"Gagal menyalin foto {photo.image.name}: {e}")

    # =================================================================
    # PASTIKAN ACTION INI ADA
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
        queryset = self.get_queryset().filter(suggester=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
