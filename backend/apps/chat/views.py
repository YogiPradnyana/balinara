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

        print("--- MEMULAI PROSES DIAGNOSTIK ---")

        try:
            bot_reply = ""

            print(f"1. Request Content-Type: {request.content_type}")

            # 2. Cek isi dari request.data (untuk data non-file)
            print(f"2. Isi request.data: {request.data}")

            # 3. Cek isi dari request.FILES (untuk data file)
            print(f"3. Isi request.FILES: {request.FILES}")

            # 4. Ambil file dan periksa tipenya
            print(f"4. Tipe objek image_file: {type(image_file)}")
            # [BARU] Buat percabangan logika
            if image_file:
                print(
                    f"5. Ukuran file awal (image_file.size): {image_file.size} bytes")
                print("6. Mencoba menjalankan image_file.seek(0)...")
                image_file.seek(0)
                print("   ... seek(0) berhasil dijalankan.")

                print(
                    f"7. Ukuran file setelah seek(0): {image_file.size} bytes")
                print("8. Memanggil process_image_query...")
                # Jika ada file gambar, panggil service untuk analisis gambar
                # Kita akan membuat fungsi ini di langkah selanjutnya
                bot_reply = process_image_query(
                    image_file=image_file,
                    user_message=user_message,
                    session_id=session_id,
                    user=request.user
                )
                print("   ... process_image_query selesai.")
            else:
                print(
                    "4a. Tidak ada 'image' di request.FILES. Masuk ke alur teks biasa.")
                # Jika tidak ada gambar, gunakan alur lama untuk teks
                bot_reply = process_chatbot_message(
                    user_message=user_message,
                    session_id=session_id,
                    user=request.user
                )

            print("--- DIAGNOSTIK SELESAI, MENGIRIM RESPONS SUKSES ---")
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
