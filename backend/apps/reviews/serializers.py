from rest_framework import serializers
# Asumsi Anda punya serializer user sederhana
from apps.users.serializers import UserSimpleSerializer
from apps.destinations.models import Destination
from .models import Review, ReviewImage, TemporaryReviewImage
import os
from django.core.files.base import ContentFile
from PIL import Image
from io import BytesIO


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ['id', 'image']


class TemporaryReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryReviewImage
        fields = ['id', 'image']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all(),
        write_only=True
    )

    images = ReviewImageSerializer(many=True, read_only=True)
    # Field untuk menerima ID gambar temporer saat POST
    image_ids = serializers.ListField(
        child=serializers.UUIDField(), write_only=True, required=False, default=list
    )

    class Meta:
        model = Review
        fields = ['id', 'user', 'destination', 'rating',
                  'comment', 'created_at', 'images', 'image_ids']
        read_only_fields = ['id', 'user', 'created_at', 'images']

    def create(self, validated_data):
        image_ids = validated_data.pop('image_ids', [])
        review = super().create(validated_data)

        # Logika untuk memindahkan gambar dari temporer ke permanen
        if image_ids:
            temp_images = TemporaryReviewImage.objects.filter(id__in=image_ids)
            images_to_process = list(temp_images)
            for temp_image in images_to_process:
                if hasattr(temp_image, 'image') and temp_image.image and os.path.exists(temp_image.image.path):
                    # Logika konversi gambar Anda sudah benar
                    pil_image = Image.open(temp_image.image)
                    buffer = BytesIO()
                    pil_image.save(buffer, format='WEBP', quality=80)
                    file_name = f"{os.path.splitext(os.path.basename(temp_image.image.name))[0]}.webp"

                    # Buat objek ReviewImage yang terhubung dengan review utama
                    ReviewImage.objects.create(
                        review=review,
                        image=ContentFile(buffer.getvalue(), name=file_name)
                    )

            # Hapus temporer satu per satu untuk memicu penghapusan file fisik
            for temp_image in images_to_process:
                temp_image.delete()
        return review
