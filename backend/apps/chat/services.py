# apps/chat/services.py

import google.generativeai as genai
import json
from django.conf import settings

from apps.destinations.models import Destination
from apps.destinations.filters import DestinationFilter
from .models import Message, ChatSession

# Konfigurasi Gemini API Anda
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(
        'gemini-1.5-flash-latest')  # Kita buat satu kali saja
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    gemini_model = None


def process_chatbot_message(user_message: str, session_id: str, user) -> str:
    if not gemini_model:
        return "Maaf, layanan chatbot sedang tidak tersedia saat ini."

    # 1. Dapatkan atau buat objek sesi dari database
    session, created = ChatSession.objects.get_or_create(id=session_id)

    if user.is_authenticated and not session.user:
        session.user = user
        session.save()

    # 2. Ambil riwayat chat yang BENAR (hanya untuk sesi ini)
    chat_history_db = Message.objects.filter(
        session=session).order_by('timestamp')

    formatted_history = []
    for msg in chat_history_db:
        # Ganti 'bot' atau nama lain menjadi 'model' agar sesuai dengan ekspektasi Gemini
        role = 'model' if msg.sender != 'user' else 'user'
        formatted_history.append({'role': role, 'parts': [msg.text]})

    try:
        # Mulai sesi chat Gemini dengan riwayat yang sudah diformat
        chat_session = gemini_model.start_chat(history=formatted_history)

        # Kirim pesan baru
        response = chat_session.send_message(user_message)
        bot_response_text = response.text

        # 3. Simpan pesan baru dengan menyertakan objek session (INI SOLUSINYA)
        Message.objects.create(
            session=session, sender='user', text=user_message)
        Message.objects.create(
            session=session, sender='model', text=bot_response_text)

        return bot_response_text

    except Exception as e:
        error_message = f"Terjadi kesalahan saat menghubungi Gemini: {str(e)}"
        print(error_message)
        # Jangan simpan pesan error ini ke database, cukup kembalikan sebagai notifikasi
        return "Maaf, sepertinya saya sedang mengalami sedikit kendala. Bisa coba tanyakan lagi?"
