# gemini_chatbot_project/chat/views.py

import google.generativeai as genai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics  # Import generics juga
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import AllowAny

# Konfigurasi API Gemini
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    # Model ini bisa diinisialisasi di sini jika tidak ada riwayat chat global yang perlu dipertahankan di luar setiap request
    # Namun, untuk mempertahankan riwayat chat antar pesan dalam satu sesi, kita akan menginisialisasi sesi chat di dalam method POST
    # model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    # Gunakan model di dalam kelas APIView
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    # model = None # Tidak perlu model global jika diinisialisasi per request

# --- API VIEWS ---


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

        # Inisialisasi model Gemini di sini atau pastikan sudah diinisialisasi global
        try:
            gemini_model = genai.GenerativeModel(
                'models/gemini-1.5-flash-latest')
        except Exception as e:
            return Response({'error': f"Error: Model Gemini tidak terkonfigurasi dengan benar. {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Ambil riwayat chat dari database untuk sesi ini (Anda mungkin perlu menambahkan 'session_id' ke model)
        # Untuk contoh ini, kita akan ambil semua chat history dari user dan bot
        # Jika Anda ingin sesi chat yang berbeda, tambahkan filter berdasarkan session_id
        chat_history_db = Message.objects.all().order_by(
            'timestamp')  # Urutkan dari yang terlama

        # Format riwayat untuk Gemini API
        formatted_history = []
        for msg in chat_history_db:
            # Perhatikan: role untuk bot di Gemini API adalah 'model', bukan 'bot'
            formatted_history.append({'role': msg.sender, 'parts': [msg.text]})

        try:
            chat_session = gemini_model.start_chat(history=formatted_history)
            response = chat_session.send_message(user_message_text)
            bot_response_text = response.text

            # Simpan pesan user ke database
            user_message_obj = Message.objects.create(
                sender='user', text=user_message_text)
            user_serializer = MessageSerializer(user_message_obj)

            # Simpan respons bot ke database
            # Pastikan sender di model Anda sesuai dengan role Gemini ('model')
            bot_message_obj = Message.objects.create(
                sender='model', text=bot_response_text)
            bot_serializer = MessageSerializer(bot_message_obj)

            # Kembalikan respons yang berisi pesan user dan bot
            return Response({
                'user_message': user_serializer.data,
                'bot_response': bot_serializer.data
            }, status=status.HTTP_200_OK)

        except Exception as e:
            error_message = f"Terjadi kesalahan saat menghubungi Gemini atau menyimpan pesan: {str(e)}"
            print(error_message)  # Untuk debugging di server
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
        # Mengembalikan 204 No Content karena tidak ada konten yang perlu dikembalikan setelah penghapusan
        return Response(status=status.HTTP_204_NO_CONTENT)
