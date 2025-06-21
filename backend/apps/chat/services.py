# apps/chat/services.py

import google.generativeai as genai
import json
from django.conf import settings
from django.db.models import Q

from apps.destinations.models import Destination
from apps.destinations.filters import DestinationFilter
from .models import Message, ChatSession

# Konfigurasi Gemini API Anda
try:
    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
    }
    genai.configure(api_key=settings.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(
        'gemini-1.5-flash-latest', safety_settings=safety_settings)  # Kita buat satu kali saja
except Exception as e:
    print(f"Error configuring Gemini API: {e}")
    gemini_model = None

# --- FUNGSI BARU (Telepon #1 - Si Pencatat) ---


def extract_entities(user_message: str) -> dict:
    """Menggunakan Gemini untuk mengekstrak kata kunci dari pesan pengguna."""
    if not gemini_model:
        return {}

    extraction_prompt = f"""
        Anda adalah asisten NLU (Natural Language Understanding) yang canggih untuk aplikasi pariwisata Bali.
        Tugas Anda adalah mengekstrak informasi dari teks pengguna dan mengubahnya menjadi format JSON yang valid.

        Database kami menggunakan nilai Bahasa Inggris.
        
        Entitas yang bisa diekstrak adalah:
        - "category_slug": Parameter slug untuk kategori dalam Bahasa Inggris. Contoh: jika pengguna mengetik 'pura', hasilnya harus 'temple'; jika 'pantai', hasilnya 'beach'; jika 'air terjun', hasilnya 'waterfall'.
        - "regency": Nama kabupaten di Bali, dengan huruf kapital di awal. Contoh: 'badung' -> 'Badung'.
        - "attribute": Kata sifat atau kualitas yang dicari (contoh: 'sepi', 'ramai', 'murah').
        
        Berikut adalah beberapa contoh cara kerjanya:
        - Teks Pengguna: "cari pura di kabupaten badung yang sepi"
        - JSON Hasil: {{"category_slug": "temple", "regency": "Badung", "attribute": "sepi"}}

        - Teks Pengguna: "info pantai di gianyar"
        - JSON Hasil: {{"category_slug": "beach", "regency": "Gianyar"}}
        
        - Teks Pengguna: "ada air terjun ga?"
        - JSON Hasil: {{"category_slug": "waterfall"}}

        Sekarang, proses teks pengguna berikut. Jawab HANYA dengan objek JSON yang valid.

        
        Teks Pengguna: "{user_message}"
        JSON Hasil:
    """
    try:
        response = gemini_model.generate_content(extraction_prompt)
        cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_text)
    except Exception:
        return {}

# --- FUNGSI BARU (Si Peneliti) ---


def get_rag_context_from_db(entities: dict) -> str:
    """Mencari data di database berdasarkan entitas dan membuat 'contekan'."""

    # Selalu mulai dengan filter untuk hanya menampilkan destinasi yang sudah di-publish
    query_filters = Q(is_published=True)

    # Membangun query secara dinamis
    if 'category_slug' in entities:
        query_filters &= Q(category__slug__icontains=entities['category_slug'])
    if 'regency' in entities:
        query_filters &= Q(address__regency__icontains=entities['regency'])
    # if 'attribute' in entities:
    #     # Jika ada atribut, kita cari di deskripsi destinasi
    #     query_filters &= Q(description__icontains=entities['attribute'])

    # Lakukan pencarian ke database
    results = Destination.objects.filter(query_filters).distinct()

    if not results.exists():
        return (
            "DATABASE_RESULT: NOT_FOUND. "
            "Ajak pengguna untuk menambahkan destinasi atau review baru di website Balinara."
        )

    # Jika ditemukan, buat rangkuman sebagai "contekan"
    context = "Berikut adalah data relevan yang ditemukan dari database Balinara:\n"
    for dest in results[:3]:  # Batasi 3 hasil teratas
        context += (
            f"- Nama: {dest.name}, Lokasi: {dest.address.regency if dest.address else 'N/A'}, "
            f"Kategori: {dest.category.name if dest.category else 'N/A'}, "
            f"Rating: {dest.average_rating}. "
            f"Harga tiket: {dest.ticket_price_range}. "
            f"Deskripsi: {dest.description[:100]}...\n"
        )
    return context

# --- FUNGSI UTAMA (Sang Manajer) ---


def process_chatbot_message(user_message: str, session_id: str, user) -> str:
    if not gemini_model:
        return "Maaf, layanan chatbot sedang tidak tersedia saat ini."

    session, _ = ChatSession.objects.get_or_create(id=session_id)

    if user.is_authenticated and not session.user:
        session.user = user
        session.save()

    entities = extract_entities(user_message)
    print(f"--- DEBUG: Entitas yang diekstrak -> {entities} ---")

    is_new_search_query = 'category_slug' in entities or 'regency' in entities or len(
        user_message.split()) > 4

    rag_context = ""  # Mulai dengan konteks kosong
    if is_new_search_query:
        print("--- DEBUG: Terdeteksi sebagai PENCARIAN BARU. Menjalankan RAG ke DB. ---")
        rag_context = get_rag_context_from_db(entities)
    else:
        print("--- DEBUG: Terdeteksi sebagai PERTANYAAN LANJUTAN. Melewatkan RAG. ---")
        # Beri tahu Gemini untuk fokus pada riwayat chat
        rag_context = "Ini adalah pertanyaan lanjutan. Jawab berdasarkan riwayat percakapan sebelumnya."

    print(f"--- DEBUG: Konteks RAG yang dibuat -> {rag_context[:200]}... ---")

    history_db = Message.objects.filter(
        session=session).order_by('-timestamp')[:6]
    formatted_history = [{'role': 'model' if msg.sender != 'user' else 'user', 'parts': [
        msg.text]} for msg in reversed(history_db)]

    # 4. Buat Jawaban Akhir dengan Konteks (Telepon #2)
    system_instruction = (
        "You are Nara, an expert tour guide for Balinara. Your personality is friendly, helpful, and like a local friend from Bali. "
        "Your primary goal is to answer user questions based on the CONTEXT provided from the Balinara database. This is your source of truth. "
        "When the context provides data, summarize it in a natural, conversational paragraph. Do not just list the data. "
        "If the context says 'DATABASE_RESULT: NOT_FOUND', you MUST politely inform the user that you couldn't find a matching destination and then warmly invite them to contribute to Balinara. "
        "Always refuse to answer questions unrelated to Bali tourism."
    )

    generation_model = genai.GenerativeModel(
        'gemini-1.5-flash-latest',
        system_instruction=system_instruction
    )
    chat_session = generation_model.start_chat(history=formatted_history)

    prompt_with_context = f"""
    CONTEXT FROM BALINARA DATABASE:
    ---
    {rag_context}
    ---
    
    USER'S QUESTION: "{user_message}"
    
    Based on the context and our previous conversation, please provide a helpful answer.
    """

    try:
        response = chat_session.send_message(prompt_with_context)
        bot_response_text = response.text

    except Exception as e:
        print(f"Error during final response generation: {e}")
        bot_response_text = "Maaf, saya sedikit bingung. Bisa coba tanyakan dengan cara lain?"

    Message.objects.create(session=session, sender='user', text=user_message)
    Message.objects.create(
        session=session, sender='model', text=bot_response_text)
    return bot_response_text
