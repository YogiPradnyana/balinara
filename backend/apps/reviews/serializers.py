from rest_framework import serializers
# Asumsi Anda punya serializer user sederhana
from apps.users.serializers import UserSimpleSerializer
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
