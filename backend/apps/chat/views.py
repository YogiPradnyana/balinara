import google.generativeai as genai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import AllowAny

# Konfigurasi API Gemini
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")


class ChatAPIView(APIView):
    """
    API endpoint untuk mengirim pesan ke Gemini dan mendapatkan respons.
    Juga mengelola riwayat chat dalam database.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_message_text = request.data.get('message')
        if not user_message_text:
            return Response({'error': 'Pesan tidak boleh kosong.'}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Gunakan system_instruction agar pembatas topik aktif sepanjang sesi
        try:
            gemini_model = genai.GenerativeModel(
                'models/gemini-1.5-flash-latest',
                system_instruction="""
Kamu adalah chatbot pariwisata Indonesia. Jawablah hanya pertanyaan seputar pariwisata seperti tempat wisata, kuliner daerah, transportasi, dan akomodasi.

Jika ada pertanyaan di luar topik pariwisata, jawab: "Maaf, saya hanya memberi informasi pariwisata."
"""
            )
        except Exception as e:
            return Response({'error': f"Error: Model Gemini tidak terkonfigurasi dengan benar. {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Ambil seluruh riwayat chat dari database (urut dari yang lama)
        chat_history_db = Message.objects.all().order_by('timestamp')

        # Format riwayat untuk Gemini API
        formatted_history = []
        for msg in chat_history_db:
            formatted_history.append({'role': msg.sender, 'parts': [msg.text]})

        try:
            # Mulai sesi chat dengan riwayat percakapan
            chat_session = gemini_model.start_chat(history=formatted_history)

            # ✅ Kirim hanya pesan user, tanpa prompt tambahan (biar konteks jalan)
            response = chat_session.send_message(user_message_text)
            bot_response_text = response.text

            # Simpan pesan user ke database
            user_message_obj = Message.objects.create(sender='user', text=user_message_text)
            user_serializer = MessageSerializer(user_message_obj)

            # Simpan respons bot ke database
            bot_message_obj = Message.objects.create(sender='model', text=bot_response_text)
            bot_serializer = MessageSerializer(bot_message_obj)

            # Kembalikan respons API
            return Response({
                'user_message': user_serializer.data,
                'bot_response': bot_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = f"Terjadi kesalahan saat menghubungi Gemini atau menyimpan pesan: {str(e)}"
            print(error_message)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MessageHistoryAPIView(generics.ListAPIView):
    """
    API endpoint untuk mendapatkan seluruh riwayat pesan.
    """
    queryset = Message.objects.all().order_by('timestamp')
    serializer_class = MessageSerializer


class ClearChatHistoryAPIView(APIView):
    """
    API endpoint untuk menghapus seluruh riwayat pesan dari database.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        Message.objects.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
