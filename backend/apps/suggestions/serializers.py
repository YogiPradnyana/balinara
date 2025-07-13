from rest_framework import serializers
from .models import Suggestion, SuggestionPhoto, TemporarySuggestionPhoto
from apps.common.models import Facility, Category

# Serializer kecil untuk data relasi (tidak perlu diubah)
class SuggestionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionPhoto
        fields = ['id', 'image']

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name']

class TemporarySuggestionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporarySuggestionPhoto
        fields = ['id', 'image']


# =================================================================
# PERBAIKAN UTAMA ADA DI DALAM SERIALIZER INI
# =================================================================
class SuggestionSerializer(serializers.ModelSerializer):
    # Field untuk menampilkan data relasi (read-only)
    photos = SuggestionPhotoSerializer(many=True, read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    suggester_username = serializers.CharField(source='suggester.username', read_only=True)
    
    # Field untuk menampilkan detail fasilitas
    facilities_details = FacilitySerializer(source='facilities', many=True, read_only=True)

    # Field untuk menerima daftar ID foto sementara dari frontend
    temp_photo_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Suggestion
        fields = [
            'id', 'name', 'category', 'category_name', 'descriptions', 'status', 
            'entrance_ticket_min', 'entrance_ticket_max', 'phone_number', 
            'email', 'street', 'sub_district', 'regency', 'latitude', 'longitude', 
            'facilities', # Untuk menerima daftar ID saat create/update
            'facilities_details', # Untuk menampilkan detail saat read
            'suggester', 'suggester_username', 'created_at', 'photos',
            'temp_photo_ids' # Hanya untuk write
        ]
        read_only_fields = ['suggester', 'created_at']

    # =================================================================
    # PERBAIKAN 1: Pindahkan method 'create' ke luar dari 'Meta'
    # dan pastikan indentasinya sejajar dengan 'class Meta'.
    # =================================================================
    def create(self, validated_data):
        # Ambil dan hapus data relasi dari validated_data sebelum membuat objek utama
        temp_photo_ids = validated_data.pop('temp_photo_ids', [])
        facilities_data = validated_data.pop('facilities', [])
        
        # Buat objek Suggestion utama dengan sisa data
        suggestion = Suggestion.objects.create(**validated_data)
        
        # Atur relasi ManyToMany untuk facilities
        suggestion.facilities.set(facilities_data)

        # Cari foto sementara berdasarkan ID dan pindahkan ke foto permanen
        temp_photos = TemporarySuggestionPhoto.objects.filter(id__in=temp_photo_ids)
        for temp_photo in temp_photos:
            SuggestionPhoto.objects.create(
                suggestion=suggestion,
                image=temp_photo.image
            )
        # Hapus foto sementara setelah dipindahkan
        temp_photos.delete()
            
        return suggestion
