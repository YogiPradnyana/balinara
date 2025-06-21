import google.generativeai as genai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import AllowAny

from .models import Message
from .serializers import MessageSerializer
from .services import process_chatbot_message


class ChatAPIView(APIView):
    """
    API endpoint untuk mengirim pesan ke Gemini dan mendapatkan respons.
    Juga mengelola riwayat chat dalam database.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user_message = request.data.get('message')
        session_id = request.data.get('session_id')

        if not user_message or not session_id:
            return Response(
                {'error': 'Fields "message" and "session_id" are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Cukup panggil service. Semua logika berat ada di sana.
            bot_reply = process_chatbot_message(
                user_message=user_message, session_id=session_id, user=request.user)
            return Response({'reply': bot_reply}, status=status.HTTP_200_OK)
        except Exception as e:
            # Ini adalah jaring pengaman terakhir jika service gagal total
            print(f"ChatAPIView Error: {e}")
            return Response(
                {'error': 'Maaf, terjadi kesalahan tak terduga di sistem kami.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MessageHistoryBySessionAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        session_id = self.kwargs.get('session_id')
        if session_id:
            # Ambil pesan yang 'id' dari 'session'-nya cocok
            return Message.objects.filter(session__id=session_id).order_by('timestamp')
        return Message.objects.none()
