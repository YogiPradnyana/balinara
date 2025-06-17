# apps/common/serializers.py
from rest_framework import serializers
from .models import Category, Facility, Address, Contact


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class FacilitySerializer(serializers.ModelSerializer):
    icon_url = serializers.SerializerMethodField(read_only=True)
    icon = serializers.FileField(
        use_url=False,
        required=False,
        allow_null=False
    )

    class Meta:
        model = Facility
        fields = ['id', 'name', 'icon_url',
                  'icon', 'slug']
        read_only_fields = ['slug', 'icon_url']

    def get_icon_url(self, obj):
        """
        Membangun URL absolut untuk ikon. Kode Anda sudah sempurna.
        """
        request = self.context.get('request')
        if obj.icon and hasattr(obj.icon, 'url'):
            return request.build_absolute_uri(obj.icon.url) if request else obj.icon.url
        return None


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        # Sebutkan field secara eksplisit untuk kontrol yang lebih baik
        fields = ['id', 'street', 'sub_district',
                  'regency', 'latitude', 'longitude']
        # Atau jika ingin semua: fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone', 'mail']  # Tambahkan 'website' jika ada
        # Atau jika ingin semua: fields = '__all__'
