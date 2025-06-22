# apps/chat/services.py

import google.generativeai as genai
import json
from django.conf import settings
from django.db.models import Q

from apps.destinations.models import Destination
from apps.destinations.filters import DestinationFilter
from .models import Message, ChatSession
from django.db.models.query import QuerySet

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


def get_rag_context_from_db(entities: dict, user_message: str) -> QuerySet:
    """
    Mencari destinasi di DB dengan logika gabungan yang lebih tangguh.
    """
    # Selalu mulai dengan queryset dasar yang sudah di-filter is_published
    base_queryset = Destination.objects.filter(is_published=True)

    # Prioritas 1: Mencari berdasarkan filter spesifik (kategori & lokasi)
    specific_filters = Q()
    if 'category_slug' in entities:
        specific_filters &= Q(
            category__slug__icontains=entities['category_slug'])
    if 'regency' in entities:
        specific_filters &= Q(address__regency__icontains=entities['regency'])

    # Jika ada filter spesifik, kita jalankan query ini dulu
    if specific_filters:
        print(
            f"--- DEBUG: Menjalankan pencarian SPESIFIK dengan filter: {specific_filters} ---")
        results = base_queryset.filter(specific_filters).distinct()

        # Jika ada atribut tambahan, saring lagi hasilnya
        if 'attribute' in entities:
            print(
                f"--- DEBUG: Menyaring hasil dengan atribut: {entities['attribute']} ---")
            results = results.filter(
                Q(name__icontains=entities['attribute']) |
                Q(description__icontains=entities['attribute'])
            )

        # Jika setelah semua filter ada hasil, kembalikan
        if results.exists():
            print(
                f"--- DEBUG: Pencarian spesifik menemukan {results.count()} hasil. ---")
            return results.order_by('-average_rating')

    # Prioritas 2 (FALLBACK): Jika pencarian spesifik tidak menemukan apa-apa,
    # atau jika dari awal tidak ada filter spesifik, lakukan pencarian umum.
    print("--- DEBUG: Menjalankan pencarian UMUM sebagai fallback. ---")

    # Gunakan seluruh pesan pengguna untuk pencarian yang lebih luas
    general_filters = (
        Q(name__icontains=user_message) |
        Q(description__icontains=user_message) |
        Q(category__name__icontains=user_message)
    )
    # Coba juga cari hanya atributnya saja jika ada
    if 'attribute' in entities:
        general_filters |= (
            Q(name__icontains=entities['attribute']) |
            Q(description__icontains=entities['attribute'])
        )

    results = base_queryset.filter(general_filters).distinct()
    print(f"--- DEBUG: Pencarian umum menemukan {results.count()} hasil. ---")

    return results.order_by('-average_rating')


# --- FUNGSI UTAMA (Sang Manajer) ---


def process_chatbot_message(user_message: str, session_id: str, user) -> str:
    if not gemini_model:
        return "Maaf, layanan chatbot sedang tidak tersedia saat ini."

    session, _ = ChatSession.objects.get_or_create(id=session_id)

    if user.is_authenticated and not session.user:
        session.user = user
        session.save()

    normalized_message = user_message.lower().strip()
    small_talk_responses = {
        "halo": "Halo! Selamat datang di Balinara. Ada yang bisa saya bantu?",
        "hai": "Hai! Ada yang bisa dibantu untuk rencana liburan di Bali?",
        "terima kasih": "Sama-sama! Senang bisa membantu.",
        "makasih": "Dengan senang hati!",
        "kamu siapa?": "Saya Nara, pemandu wisata virtual dari Balinara!"
    }
    if normalized_message in small_talk_responses:
        # Kita tetap simpan ke riwayat, tapi balasannya instan
        session, _ = ChatSession.objects.get_or_create(id=session_id)
        Message.objects.create(
            session=session, sender='user', text=user_message)
        bot_reply = small_talk_responses[normalized_message]
        Message.objects.create(session=session, sender='model', text=bot_reply)
        return bot_reply

    entities = extract_entities(user_message)
    is_new_search_query = 'category_slug' in entities or 'regency' in entities or len(
        user_message.split()) > 4

    rag_context = ""
    if is_new_search_query:
        results = get_rag_context_from_db(entities, user_message)
        print(results)
        if results.exists():
            rag_context = "Berikut data relevan dari database Balinara:\n"
            context_to_save = []
            for dest in results[:3]:
                rag_context += (
                    f"- Nama: {dest.name}, "
                    f"Lokasi: {dest.address.regency if dest.address else 'N/A'}, "
                    f"Kategori: {dest.category.name if dest.category else 'N/A'}, "
                    f"Rating: {dest.average_rating}, "
                    f"Harga Tiket: {dest.ticket_price_range or '-'}.\n"
                    # f"Deskripsi: {dest.description[:100]}...\n" # Deskripsi bisa ditambahkan jika perlu
                )

                # 2. Buat juga 'context_to_save' yang kaya untuk ingatan follow-up
                context_to_save.append({
                    'name': dest.name,
                    'average_rating': float(dest.average_rating),
                    'ticket_price_range': dest.ticket_price_range,
                    # Simpan deskripsi untuk nanti
                    'description_snippet': dest.description[:100]
                })

            session.active_context = {'destinations': context_to_save}
            session.save()
        else:
            rag_context = "DATABASE_RESULT: NOT_FOUND, lalu Ajak pengguna untuk menambahkan destinasi atau review baru di website Balinara."

            session.active_context = {}
            session.save()
    else:
        active_context_data = session.active_context or {}
        destinations_in_context = active_context_data.get('destinations', [])
        if destinations_in_context:
            rag_context = "Ini pertanyaan lanjutan. Konteks saat ini adalah tentang destinasi:\n"
            for dest in destinations_in_context:
                rag_context += f"- Nama: {dest['name']}, Rating: {dest['average_rating']}, Tiket: {dest['ticket_price_range']}\n"
        else:
            rag_context = "Ini pertanyaan lanjutan tanpa konteks aktif."

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
