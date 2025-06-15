# apps/common/serializers.py
from rest_framework import serializers
from .models import Category, Facility, Address, Contact


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']
        read_only_fields = ['slug']


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ['id', 'name', 'icon_url']  # Atau 'icon_image'


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
