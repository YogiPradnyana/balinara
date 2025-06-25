import google.generativeai as genai
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import Message
from .serializers import MessageSerializer
from rest_framework.permissions import AllowAny
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Message
from .serializers import MessageSerializer
from .services import process_chatbot_message, process_image_query


class ChatAPIView(APIView):
    """
    API endpoint untuk mengirim pesan ke Gemini dan mendapatkan respons.
    Juga mengelola riwayat chat dalam database.
    """
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        image_file = request.FILES.get('image', None)
        user_message = request.data.get('message')
        session_id = request.data.get('session_id')

        if not session_id:
            return Response(
                {'error': 'Field "session_id" is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validasi user_message (jika tidak ada gambar, maka pesan wajib ada)
        if not image_file and not user_message:
            return Response(
                {'error': 'Either "message" or "image" must be provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if image_file:
            MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB
            if image_file.size > MAX_UPLOAD_SIZE:
                logger.warning(
                    f"User tried to upload a file larger than the limit. "
                    f"File size: {image_file.size} bytes."
                )
                return Response(
                    {"error": "Ukuran file gambar tidak boleh melebihi 5MB."},
                    status=status.HTTP_400_BAD_REQUEST  # Error 400 Bad Request
                )

        try:
            bot_reply = ""
            user_message_obj = None

            if image_file:
                image_file.seek(0)
                bot_reply, user_message_obj = process_image_query(
                    image_file=image_file,
                    user_message=user_message,
                    session_id=session_id,
                    user=request.user
                )
            else:
                bot_reply, user_message_obj = process_chatbot_message(
                    user_message=user_message,
                    session_id=session_id,
                    user=request.user
                )

            bot_message_obj = Message.objects.create(
                session=user_message_obj.session,
                sender='model',
                text=bot_reply
            )

            user_message_data = MessageSerializer(user_message_obj).data
            bot_message_data = MessageSerializer(bot_message_obj).data

            return Response({
                "user_message_final": user_message_data,
                "bot_reply": bot_message_data
            }, status=status.HTTP_200_OK)

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
