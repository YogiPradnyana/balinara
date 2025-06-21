# gemini_chatbot_project/chat/urls.py

from django.urls import path
# IMPOR HANYA CLASS-CLASS API VIEW YANG BARU ANDA BUAT
from .views import ChatAPIView, MessageHistoryBySessionAPIView

app_name = 'chat_api'

urlpatterns = [
    # Endpoint untuk mengirim pesan dan mendapatkan respons Gemini
    # Perhatikan: path() di sini tidak memiliki 'api/' di depannya,
    # karena sudah ditambahkan di urls.py utama proyek.
    path('send/', ChatAPIView.as_view(), name='send_message'),

    # Endpoint BARU untuk mengambil riwayat berdasarkan session_id
    path('history/<uuid:session_id>/', MessageHistoryBySessionAPIView.as_view(),
         name='message_history_by_session'),
]
