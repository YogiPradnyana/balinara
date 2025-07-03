# gemini_chatbot_project/chat/serializers.py

from rest_framework import serializers
from .models import Message, ChatSession


class MessageSerializer(serializers.ModelSerializer):
    session_id = serializers.UUIDField(source='session.id', read_only=True)

    class Meta:
        model = Message
        # Tentukan field yang ingin diekspos
        fields = ['id', 'session_id', 'sender', 'text', 'timestamp', 'image']
        # Atau 'fields = '__all__' untuk mengekspos semua field

    def get_image(self, obj):
        """
        Method ini akan dipanggil secara otomatis untuk setiap objek Message.
        Tugasnya adalah untuk menghasilkan nilai untuk field 'image'.
        """
        # Cek jika field 'image' pada objek Message (obj) memiliki file
        if obj.image and hasattr(obj.image, 'url'):
            # Minta URL publiknya dari Cloudinary. Atribut .url inilah kuncinya.
            return obj.image.url

        # Jika tidak ada gambar, kembalikan null
        return None


class ChatSessionSerializer(serializers.ModelSerializer):
    # Saat kita lihat detail sesi, kita juga ingin lihat pesannya
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'created_at', 'messages']
