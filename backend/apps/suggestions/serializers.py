# apps/suggestions/serializers.py
from rest_framework import serializers
from .models import Suggestion, SuggestionPhoto
from apps.common.models import Facility

# Serializer ini hampir identik dengan DestinationSerializer sebelumnya
class SuggestionSerializer(serializers.ModelSerializer):
    uploaded_photos = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True, required=False
    )
    facilities = serializers.PrimaryKeyRelatedField(
        queryset=Facility.objects.all(),
        many=True, required=False
    )

    class Meta:
        model = Suggestion
        # Kita hanya butuh field yang bisa diisi user, status diatur otomatis
        fields = [
            'id', 'name', 'category', 'descriptions', 
            'entrance_ticket_min', 'entrance_ticket_max', 'phone_number', 'email',
            'street', 'sub_district', 'regency', 'latitude', 'longitude',
            'facilities', 'uploaded_photos'
        ]

    def create(self, validated_data):
        uploaded_photos_data = validated_data.pop('uploaded_photos', [])
        facilities_data = validated_data.pop('facilities', [])
        
        suggestion = Suggestion.objects.create(**validated_data)
        
        if facilities_data:
            suggestion.facilities.set(facilities_data)
            
        for photo_data in uploaded_photos_data:
            SuggestionPhoto.objects.create(suggestion=suggestion, image=photo_data)
            
        return suggestion