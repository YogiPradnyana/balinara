# apps/destinations/serializers.py
from rest_framework import serializers
from .models import Destination, DestinationImage
# Impor model dari common
from apps.common.models import Category, Address, Contact, Facility
from apps.common.serializers import (  # Impor serializer dari common
    CategorySerializer,
    AddressSerializer,
    ContactSerializer,
    FacilitySerializer
)


class DestinationImageSerializer(serializers.ModelSerializer):
    # image_url akan memberikan URL absolut ke gambar
    image_url = serializers.SerializerMethodField(read_only=True)
    # image field akan digunakan untuk upload dan akan berisi path relatif saat dibaca (jika use_url=False)
    # atau URL jika use_url=True (default). Untuk create/update, kita ingin menerima file.
    # use_url=False agar saat create/update tidak error jika request bukan dari context view
    image = serializers.ImageField(use_url=False, required=True)

    class Meta:
        model = DestinationImage
        fields = ['id', 'image', 'image_url',
                  'alt_text', 'is_primary', 'uploaded_at']
        # image_url dan uploaded_at dibuat otomatis
        read_only_fields = ('id', 'image_url', 'uploaded_at')

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url) if request else obj.image.url
        return None

    def validate_image(self, value):
        # Contoh validasi ukuran file (misalnya, maks 2MB)
        if value.size > 2 * 1024 * 1024:  # 2MB
            raise serializers.ValidationError("Image size cannot exceed 2MB.")
        # Anda bisa menambahkan validasi tipe file di sini jika perlu,
        # meskipun ImageField sudah melakukan beberapa validasi dasar.
        return value


class DestinationListSerializer(serializers.ModelSerializer):
    """
    Serializer untuk daftar destinasi (tampilan lebih ringkas).
    """
    category = CategorySerializer(read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    # Misal hanya menampilkan Kabupaten/Kota
    address_brief = serializers.SerializerMethodField()

    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'average_rating', 'total_reviews',
            'category', 'primary_image_url', 'address_brief', 'is_published'
        ]

    def get_primary_image_url(self, obj):
        request = self.context.get('request')
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image and primary_image.image and hasattr(primary_image.image, 'url'):
            return request.build_absolute_uri(primary_image.image.url) if request else primary_image.image.url
        # Fallback ke gambar pertama jika tidak ada primary
        # Ambil gambar pertama yang diupload
        first_image = obj.images.order_by('uploaded_at').first()
        if first_image and first_image.image and hasattr(first_image.image, 'url'):
            return request.build_absolute_uri(first_image.image.url) if request else first_image.image.url
        return None  # Atau URL ke gambar placeholder default

    def get_address_brief(self, obj):
        if obj.address:
            return f"{obj.address.regency}"  # Contoh, bisa juga provinsi
        return None


class DestinationDetailSerializer(serializers.ModelSerializer):
    """
    Serializer untuk detail destinasi (tampilan lebih lengkap, termasuk create/update).
    """
    category = CategorySerializer(read_only=True)  # Untuk GET request
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=False, allow_null=True
    )

    # Untuk GET, dan untuk nested create/update
    address = AddressSerializer(required=False, allow_null=True)
    # Untuk GET, dan untuk nested create/update
    contact = ContactSerializer(required=False, allow_null=True)

    facilities = FacilitySerializer(
        many=True, read_only=True)  # Untuk GET request
    facility_ids = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(), source='facilities', write_only=True, many=True, required=False
    )

    images = DestinationImageSerializer(
        many=True, read_only=True)  # Untuk GET request
    # Untuk upload gambar baru saat membuat/mengupdate destinasi,
    # kita akan menggunakan action terpisah atau menangani `request.FILES` di view.
    # Atau, Anda bisa menambahkan field ListField dari ImageField di sini, tapi itu bisa jadi rumit.

    # Field yang hanya dibaca (dihitung atau di-set oleh sistem)
    average_rating = serializers.DecimalField(
        max_digits=3, decimal_places=2, read_only=True)
    total_reviews = serializers.IntegerField(read_only=True)

    class Meta:
        model = Destination
        fields = [
            'id', 'name', 'slug', 'description', 'ticket_price_range', 'operational_hours',
            'average_rating', 'total_reviews',
            'category', 'category_id',  # category untuk read, category_id untuk write
            'address',
            'contact',
            'facilities', 'facility_ids',  # facilities untuk read, facility_ids untuk write
            'images',
            'is_published',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'slug', 'average_rating',
                            'total_reviews', 'created_at', 'updated_at', 'images')
        # 'slug' akan dibuat otomatis oleh model.
        # 'images' akan dikelola melalui endpoint/action terpisah atau setelah destinasi dibuat.

    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        contact_data = validated_data.pop('contact', None)
        # 'facilities' sudah di-handle oleh source='facilities' di facility_ids
        # dan akan otomatis di-set oleh DRF jika facility_ids dikirim.

        address_instance = None
        if address_data:
            address_instance = Address.objects.create(**address_data)

        contact_instance = None
        if contact_data:
            contact_instance = Contact.objects.create(**contact_data)

        destination = Destination.objects.create(
            address=address_instance,
            contact=contact_instance,
            **validated_data
        )
        # Fasilitas sudah di-set jika facility_ids ada di validated_data
        return destination

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', None)
        contact_data = validated_data.pop('contact', None)
        # 'facilities' di-handle oleh source='facilities' dari facility_ids

        # Update Address
        if address_data:
            if instance.address:
                # Update field-field address yang ada
                for attr, value in address_data.items():
                    setattr(instance.address, attr, value)
                instance.address.save()
            else:  # Jika destinasi belum punya alamat, buat baru
                instance.address = Address.objects.create(**address_data)
        elif 'address' in validated_data and validated_data['address'] is None:
            # Jika frontend mengirim null untuk address (menghapus alamat)
            if instance.address:
                instance.address.delete()  # Hapus objek Address terkait
            instance.address = None

        # Update Contact
        if contact_data:
            if instance.contact:
                for attr, value in contact_data.items():
                    setattr(instance.contact, attr, value)
                instance.contact.save()
            else:
                instance.contact = Contact.objects.create(**contact_data)
        elif 'contact' in validated_data and validated_data['contact'] is None:
            if instance.contact:
                instance.contact.delete()
            instance.contact = None

        # Update field-field Destination lainnya
        # fasilitas akan diupdate secara otomatis oleh DRF karena 'facility_ids'
        # dan source='facilities'
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
