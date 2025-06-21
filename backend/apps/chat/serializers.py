# gemini_chatbot_project/chat/serializers.py

from rest_framework import serializers
from .models import Message, ChatSession


class MessageSerializer(serializers.ModelSerializer):
    session_id = serializers.UUIDField(source='session.id', read_only=True)

    class Meta:
        model = Message
        # Tentukan field yang ingin diekspos
        fields = ['id', 'session_id', 'sender', 'text', 'timestamp']
        # Atau 'fields = '__all__' untuk mengekspos semua field


class ChatSessionSerializer(serializers.ModelSerializer):
    # Saat kita lihat detail sesi, kita juga ingin lihat pesannya
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'created_at', 'messages']
