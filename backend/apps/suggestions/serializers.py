from rest_framework import serializers
from .models import Suggestion, SuggestionPhoto

# Serializer kecil ini khusus untuk mengubah data setiap foto menjadi format JSON
class SuggestionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionPhoto
        fields = ['id', 'image']


class SuggestionSerializer(serializers.ModelSerializer):
    # Field ini untuk menampilkan data relasi (read-only)
    # Ini akan berisi daftar objek foto yang sudah diformat oleh SuggestionPhotoSerializer
    photos = SuggestionPhotoSerializer(many=True, read_only=True)
    
    # Field ini untuk menampilkan nama kategori, bukan hanya ID-nya
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    # Field ini untuk menampilkan username pengusul
    suggester_username = serializers.CharField(source='suggester.username', read_only=True)

    class Meta:
        model = Suggestion
        # Daftar semua field dari model yang ingin kita kirim atau terima.
        # 'suggester' tidak perlu ada di sini untuk 'create' karena diisi otomatis oleh view.
        fields = [
            'id',
            'name',
            'category',       # Untuk menerima ID saat membuat (write)
            'category_name',  # Untuk menampilkan nama saat membaca (read)
            'descriptions',
            'entrance_ticket_min',
            'entrance_ticket_max',
            'phone_number',
            'email',
            'street',
            'sub_district',
            'regency',
            'latitude',
            'longitude',
            'facilities',     # Untuk menerima daftar ID fasilitas saat membuat (write)
            'suggester',      # Untuk menampilkan ID user (read-only)
            'suggester_username', # Untuk menampilkan username (read-only)
            'status',
            'created_at',
            'photos',         # Untuk menampilkan daftar foto (read-only)
        ]
        # Membuat beberapa field hanya bisa dibaca (read-only)
        read_only_fields = ['suggester', 'status', 'created_at']

    def create(self, validated_data):
        """
        Override method create untuk menangani relasi ManyToMany (facilities)
        dan upload foto secara manual dari data request.
        """
        # Pisahkan data 'facilities' dari data utama
        facilities_data = validated_data.pop('facilities', [])
        
        # Buat objek Suggestion terlebih dahulu
        suggestion = Suggestion.objects.create(**validated_data)
        
        # Atur relasi ManyToMany untuk facilities
        suggestion.facilities.set(facilities_data)

        # Ambil file foto dari context request yang dikirim oleh view
        # dan buat objek SuggestionPhoto untuk setiap fotonya
        photos_data = self.context['request'].FILES.getlist('uploaded_photos')
        for photo_data in photos_data:
            SuggestionPhoto.objects.create(suggestion=suggestion, image=photo_data)
            
        return suggestion