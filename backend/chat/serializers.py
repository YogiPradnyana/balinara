# gemini_chatbot_project/chat/serializers.py

from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'timestamp'] # Tentukan field yang ingin diekspos
        # Atau 'fields = '__all__' untuk mengekspos semua field