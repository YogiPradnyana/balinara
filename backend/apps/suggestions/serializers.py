from rest_framework import serializers
from .models import Suggestion, SuggestionPhoto, TemporarySuggestionPhoto
from apps.common.models import Facility, Category

# Serializer kecil untuk data relasi (sudah bagus, hanya tambahkan CategorySerializer)
class SuggestionPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestionPhoto
        fields = ['id', 'image']

class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name'] # Pastikan ini mengembalikan ID dan nama kategori

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
    suggester_username = serializers.CharField(source='suggester.username', read_only=True)
    
    # --- PERBAIKAN 1: Tambahkan CategorySerializer untuk output multiple categories ---
    # Gunakan nama yang konsisten dengan frontend (categories_details)
    categories_details = CategorySerializer(source='categories', many=True, read_only=True)

    # Field untuk menampilkan detail fasilitas (sudah benar)
    facilities_details = FacilitySerializer(source='facilities', many=True, read_only=True)

    # Field untuk menerima daftar ID foto sementara dari frontend (sudah benar)
    temp_photo_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False
    )

    # --- PERBAIKAN 2: Field untuk menerima daftar ID kategori dari frontend ---
    # Ini adalah field write-only yang menerima array ID kategori
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), # Pastikan queryset ini benar
        many=True, # Penting untuk ManyToMany
        write_only=True, # Hanya untuk input
        required=False # Sesuaikan dengan kebutuhan validasi Anda
    )

    # --- PERBAIKAN 3: Field untuk menerima daftar ID fasilitas dari frontend ---
    # Jika Anda ingin menerima ID fasilitas secara terpisah saat write (seperti categories)
    # Ini sudah ada di `Meta.fields`, tapi kita perlu memastikan handlingnya di `create`/`update`
    facilities = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(), # Pastikan queryset ini benar
        many=True, # Penting untuk ManyToMany
        write_only=True, # Hanya untuk input
        required=False
    )


    class Meta:
        model = Suggestion
        fields = [
            'id', 'name', 
            # --- Perubahan di `fields`: Hapus 'category' dan 'category_name' ---
            # Tambahkan 'categories_details' untuk output dan 'categories' untuk input
            'categories', # Field write-only untuk menerima ID
            'categories_details', # Field read-only untuk detail objek
            
            'descriptions', 'status',
            'entrance_ticket_min', 'entrance_ticket_max', 'phone_number', 
            'email', 'street', 'sub_district', 'regency', 'latitude', 'longitude', 
            
            'facilities', # Field write-only untuk menerima ID
            'facilities_details', # Field read-only untuk detail objek (sudah benar)
            
            'suggester', 'suggester_username', 'created_at', 'photos',
            'temp_photo_ids' # Hanya untuk write
        ]
        read_only_fields = ['suggester', 'created_at']


    # --- PERBAIKAN 4: Pindahkan method 'create' dan 'update' ke luar dari 'Meta' ---
    # dan pastikan indentasinya sejajar dengan 'class Meta'.
    # Ini akan override metode create bawaan ModelSerializer.
    def create(self, validated_data):
        # Ambil dan hapus data relasi dari validated_data sebelum membuat objek utama
        temp_photo_ids = validated_data.pop('temp_photo_ids', [])
        facilities_data = validated_data.pop('facilities', [])
        categories_data = validated_data.pop('categories', []) # Ambil data categories

        # Buat objek Suggestion utama dengan sisa data
        suggestion = Suggestion.objects.create(**validated_data)
        
        # Atur relasi ManyToMany untuk facilities
        if facilities_data: # Pastikan ada data sebelum mencoba set
            suggestion.facilities.set(facilities_data)

        # Atur relasi ManyToMany untuk categories
        if categories_data: # Pastikan ada data sebelum mencoba set
            suggestion.categories.set(categories_data)

        # Cari foto sementara berdasarkan ID dan pindahkan ke foto permanen
        temp_photos = TemporarySuggestionPhoto.objects.filter(id__in=temp_photo_ids)
        for temp_photo in temp_photos:
            SuggestionPhoto.objects.create(
                suggestion=suggestion,
                image=temp_photo.image # Ini akan menyalin file
            )
        # Hapus foto sementara setelah dipindahkan
        temp_photos.delete()
            
        return suggestion

    # Tambahkan metode update() untuk menangani pembaruan data yang terkait
    def update(self, instance, validated_data):
        # Ambil data relasi jika ada di validated_data
        temp_photo_ids = validated_data.pop('temp_photo_ids', None)
        facilities_data = validated_data.pop('facilities', None)
        categories_data = validated_data.pop('categories', None)

        # Update field-field biasa pada instance Suggestion
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save() # Simpan perubahan field biasa

        # Update relasi ManyToMany untuk facilities
        if facilities_data is not None:
            instance.facilities.set(facilities_data)

        # Update relasi ManyToMany untuk categories
        if categories_data is not None:
            instance.categories.set(categories_data)

        # Tambahkan/hapus foto terkait jika temp_photo_ids diberikan
        if temp_photo_ids is not None:
            # Anda bisa memilih untuk menghapus semua foto lama dan menambahkan yang baru
            # Atau, mengelola penambahan/penghapusan secara lebih granular.
            # Contoh: Hapus semua foto suggestion yang ada dan tambahkan yang baru dari temp_photo_ids
            instance.photos.all().delete() # Hapus semua foto suggestion yang ada
            temp_photos = TemporarySuggestionPhoto.objects.filter(id__in=temp_photo_ids)
            for temp_photo in temp_photos:
                SuggestionPhoto.objects.create(
                    suggestion=instance,
                    image=temp_photo.image
                )
            temp_photos.delete() # Hapus foto sementara setelah dipindahkan

        return instance