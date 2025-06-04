# gemini_chatbot_project/chat/urls.py

from django.urls import path
# IMPOR HANYA CLASS-CLASS API VIEW YANG BARU ANDA BUAT
from .views import ChatAPIView, MessageHistoryAPIView, ClearChatHistoryAPIView

urlpatterns = [
    # Endpoint untuk mengirim pesan dan mendapatkan respons Gemini
    # Perhatikan: path() di sini tidak memiliki 'api/' di depannya,
    # karena sudah ditambahkan di urls.py utama proyek.
    path('chat/', ChatAPIView.as_view(), name='gemini-chat-api'),

    # Endpoint untuk mendapatkan seluruh riwayat pesan
    path('messages/', MessageHistoryAPIView.as_view(), name='message-history-api'),

    # Endpoint untuk menghapus riwayat pesan
    path('clear_history/', ClearChatHistoryAPIView.as_view(), name='clear-chat-history-api'),
]