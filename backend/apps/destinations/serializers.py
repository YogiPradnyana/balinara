import os
from PIL import Image
from io import BytesIO
from rest_framework import serializers
# Untuk atomic transaction saat create/update nested
from django.db import transaction
from django.core.files.base import ContentFile
from .models import Destination, DestinationImage, TemporaryImage
from apps.common.models import Category, Address, Contact, Facility
from apps.common.serializers import (
    CategorySerializer,
    AddressSerializer,
    ContactSerializer,
    FacilitySerializer
)

# --- Serializer untuk DestinationImage ---


class DestinationImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(
        use_url=False, required=True, allow_empty_file=False)
    # 'destination' akan di-set oleh view saat upload melalui action, jadi tidak perlu di sini saat create
    # Jika serializer ini digunakan untuk nested create di DestinationDetailSerializer, maka perlu
    # Namun, kita akan handle upload gambar via action terpisah untuk kesederhanaan.

    class Meta:
        model = DestinationImage
        fields = ['id', 'image', 'image_url',
                  'alt_text', 'is_primary', 'uploaded_at']
        read_only_fields = ('id', 'image_url', 'uploaded_at')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:  # Maks 5MB
            raise serializers.ValidationError("Image size cannot exceed 5MB.")
        return value

# --- Serializer untuk Daftar Destinasi (Ringkas) ---


class DestinationListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    address = AddressSerializer(read_only=True)
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'average_rating', 'total_reviews',
            'category', 'primary_image_url', 'address', 'contact', 'is_published'
        ]
        read_only_fields = ('id', 'slug', 'average_rating',
                            'total_reviews', 'primary_image_url', 'address')

    def get_primary_image_url(self, obj):
        # ... (logika sama seperti sebelumnya) ...
        request = self.context.get('request')
        primary_image = obj.images.filter(is_primary=True).first()
        if not primary_image:
            primary_image = obj.images.order_by('uploaded_at').first()
        if primary_image and primary_image.image and hasattr(primary_image.image, 'url'):
            return request.build_absolute_uri(primary_image.image.url) if request else primary_image.image.url
        return None


class TemporaryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryImage
        fields = ['id', 'image', 'uploaded_at']
        read_only_fields = ('id', 'uploaded_at',)

# --- Serializer untuk Detail, Create, dan Update Destinasi ---


class DestinationDetailCRUDSerializer(serializers.ModelSerializer):
    # --- READ-ONLY fields (untuk GET response) ---
    categories = CategorySerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)
    contact = ContactSerializer(read_only=True)
    facilities = FacilitySerializer(many=True, read_only=True)
    images = DestinationImageSerializer(
        many=True, read_only=True)  # Gambar dikelola via action

    # --- WRITE-ONLY fields (untuk POST/PUT/PATCH request) ---
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='categories',  # Hubungkan ke field 'categories' di model
        write_only=True,
        many=True,            # Izinkan banyak ID
        required=False        # Buat opsional
    )

    # Untuk Address dan Contact, kita akan terima data nested dan proses di create/update
    address_data = AddressSerializer(
        write_only=True, required=False)
    contact_data = ContactSerializer(
        write_only=True, required=False, allow_null=True)

    facility_ids = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(), source='facilities', write_only=True,
        many=True, required=False
    )

    image_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        required=False, default=list
    )

    delete_image_ids = serializers.ListField(
        child=serializers.IntegerField(),  # ID gambar adalah integer
        write_only=True,
        required=False, default=list
    )

    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'description', 'ticket_price_range',
            'average_rating', 'total_reviews', 'is_published',
            # Read-only representasi
            'categories', 'address', 'contact', 'facilities', 'images',
            # Write-only/input fields
            'category_ids', 'address_data', 'contact_data', 'facility_ids', 'image_ids',
            'delete_image_ids', 'created_at', 'updated_at'
        ]
        read_only_fields = (
            'id', 'slug', 'average_rating', 'total_reviews', 'created_at', 'updated_at',
            'images',  # images dikelola oleh action terpisah
            # Field di bawah ini adalah representasi objek, bukan input langsung untuk create/update utama
            'categories', 'address', 'contact', 'facilities'
        )
        # Slug akan dibuat otomatis oleh model.

    def _handle_nested_one_to_one_write(self, instance_field_obj, nested_data_dict, NestedModel):
        """Helper untuk create/update/delete nested OneToOne (Address, Contact) saat write."""
        if nested_data_dict is None:  # Klien mengirim null -> hapus jika ada
            if instance_field_obj:
                instance_field_obj.delete()
            return None
        elif nested_data_dict:  # Klien mengirim data objek
            # Hapus ID jika ada di nested_data_dict karena kita tidak ingin error jika ID tidak cocok
            # atau jika ini adalah pembuatan objek baru.
            nested_data_dict.pop('id', None)
            if instance_field_obj:  # Update yang ada
                for attr, value in nested_data_dict.items():
                    setattr(instance_field_obj, attr, value)
                instance_field_obj.save()
                return instance_field_obj
            else:  # Buat baru
                return NestedModel.objects.create(**nested_data_dict)
        return instance_field_obj  # Tidak ada perubahan pada field nested ini

    def _handle_new_images(self, destination_instance, image_ids):
        """Fungsi helper terpisah untuk memproses gambar baru."""
        if not image_ids:
            return

        temp_images = TemporaryImage.objects.filter(id__in=image_ids)
        temp_images_to_process = list(temp_images)

        for temp_image in temp_images:
            if not os.path.exists(temp_image.image.path):
                continue

            pil_image = Image.open(temp_image.image)
            buffer = BytesIO()
            pil_image.save(buffer, format='WEBP', quality=85)

            # Buat nama file baru dengan ekstensi .webp
            original_filename = os.path.splitext(
                os.path.basename(temp_image.image.name))[0]
            new_filename = f"{original_filename}.webp"
            # -------------------------------------------

            destination_image = DestinationImage(
                destination=destination_instance,
                alt_text=f"Image for {destination_instance.name}"
            )

            # Simpan konten WEBP dari buffer sebagai file baru di lokasi final
            destination_image.image.save(
                new_filename, ContentFile(buffer.getvalue()), save=True
            )

        for temp_image in temp_images_to_process:
            temp_image.delete()

    @transaction.atomic  # Pastikan operasi database bersifat atomic
    def create(self, validated_data):
        validated_data.pop('delete_image_ids', None)
        image_ids = validated_data.pop('image_ids', [])
        address_data = validated_data.pop('address_data', None)
        contact_data = validated_data.pop('contact_data', None)
        categories_qs = validated_data.pop('categories', [])
        facilities_qs = validated_data.pop('facilities', [])

        address_instance = self._handle_nested_one_to_one_write(
            None, address_data, Address)
        contact_instance = self._handle_nested_one_to_one_write(
            None, contact_data, Contact)

        destination = Destination.objects.create(
            address=address_instance,
            contact=contact_instance,
            **validated_data
        )
        if categories_qs:
            destination.categories.set(categories_qs)
        if facilities_qs:
            destination.facilities.set(facilities_qs)

        # Gunakan fungsi helper
        self._handle_new_images(destination, image_ids)

        return destination

    @transaction.atomic
    def update(self, instance, validated_data):
        # Ambil image_ids dari data yang divalidasi, jika ada.
        image_ids_to_add = validated_data.pop('image_ids', [])
        image_ids_to_delete = validated_data.pop('delete_image_ids', [])

        # Hapus gambar yang ditandai untuk dihapus
        if image_ids_to_delete:
            images_to_delete = instance.images.filter(
                id__in=image_ids_to_delete)
            for image in images_to_delete:
                image.delete()

        # Handle nested Address and Contact
        if 'address_data' in validated_data:
            address_data = validated_data.pop('address_data')
            instance.address = self._handle_nested_one_to_one_write(
                instance.address, address_data, Address)

        if 'contact_data' in validated_data:
            contact_data = validated_data.pop('contact_data')
            instance.contact = self._handle_nested_one_to_one_write(
                instance.contact, contact_data, Contact)

        # Update instance dengan data lainnya
        instance = super().update(instance, validated_data)

        # Tambahkan gambar baru menggunakan fungsi helper yang sama
        self._handle_new_images(instance, image_ids_to_add)

        return instance
