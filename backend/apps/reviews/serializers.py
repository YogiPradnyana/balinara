from rest_framework import serializers
# Asumsi Anda punya serializer user sederhana
from apps.users.serializers import UserSimpleSerializer
from apps.destinations.models import Destination
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    destination = serializers.PrimaryKeyRelatedField(
        queryset=Destination.objects.all(),
        write_only=True
    )

    class Meta:
        model = Review
        fields = ['id', 'user', 'destination',
                  'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
