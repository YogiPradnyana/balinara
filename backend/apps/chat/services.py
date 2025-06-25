# apps/chat/services.py

import google.generativeai as genai
import json
import logging
import io
from PIL import Image
from django.conf import settings
from django.db.models import Q

from apps.destinations.models import Destination
from apps.destinations.filters import DestinationFilter
from .models import Message, ChatSession
from django.db.models.query import QuerySet


logger = logging.getLogger(__name__)

EXTRACTION_PROMPT_TEMPLATE = """
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

FINAL_RESPONSE_SYSTEM_INSTRUCTION = (
    "You are Nara, an expert tour guide for Balinara. Your personality is friendly, helpful, and like a local friend from Bali. "
    "Your primary goal is to answer user questions based on the CONTEXT provided from the Balinara database. This is your source of truth. "
    "When the context provides data, summarize it in a natural, conversational paragraph. Do not just list the data. "
    "If the context says 'DATABASE_RESULT: NOT_FOUND', your first step is to politely state that you don't have a specific partner recommendation from Balinara. "
    "HOWEVER, after stating that, you MUST then use your own general knowledge about Bali to provide a helpful, alternative recommendation. "
    "Try to list at least 3-5 specific places, if you know them from your training data. "
    "Frame this as a general suggestion to help the user, not a formal Balinara endorsement. Be confident in your general knowledge."
    "Always refuse to answer questions unrelated to Bali tourism."
)

SMALL_TALK_RESPONSES = {
    "halo": "Halo! Selamat datang di Balinara. Ada yang bisa saya bantu?",
    "hai": "Hai! Ada yang bisa dibantu untuk rencana liburan di Bali?",
    "terima kasih": "Sama-sama! Senang bisa membantu.",
    "makasih": "Dengan senang hati!",
    "kamu siapa?": "Saya Nara, pemandu wisata virtual dari Balinara!"
}


try:
    safety_settings = {
        "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
        "HARM_CATEGORY_HATE_SPEECH": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_MEDIUM_AND_ABOVE",
        "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_MEDIUM_AND_ABOVE",
    }
    genai.configure(api_key=settings.GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel(
        'gemini-1.5-flash-latest',
        safety_settings=safety_settings
    )
except Exception as e:
    logger.error(f"Error configuring Gemini API: {e}")
    gemini_model = None


def extract_entities(user_message: str) -> dict:
    """Menggunakan Gemini untuk mengekstrak kata kunci dari pesan pengguna."""
    if not gemini_model:
        return {}

    prompt = EXTRACTION_PROMPT_TEMPLATE.format(user_message=user_message)
    try:
        response = gemini_model.generate_content(prompt)
        cleaned_text = response.text.strip().replace('```json', '').replace('```', '')
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        logger.warning(
            f"Failed to decode JSON from Gemini: {e}. Raw text: {response.text}")
        return {}
    except Exception as e:
        logger.error(f"Error in extract_entities: {e}")
        return {}


def get_rag_context_from_db(entities: dict, user_message: str, target_name: str = None) -> QuerySet:
    """
    Mencari destinasi di DB dengan logika gabungan yang lebih tangguh.
    """
    base_queryset = Destination.objects.select_related(
        'address').prefetch_related('categories').filter(is_published=True)

    if target_name:
        logger.debug(f"Menjalankan pencarian TARGETED untuk: {target_name}")
        return base_queryset.filter(name__icontains=target_name).distinct().order_by('-average_rating')

    # Prioritas 1: Mencari berdasarkan filter spesifik (kategori & lokasi)
    specific_filters = Q()
    if 'category_slug' in entities:
        # [REVISI] Gunakan 'categories' (jamak) untuk ManyToMany
        specific_filters &= Q(
            categories__slug__icontains=entities['category_slug'])
    if 'regency' in entities:
        specific_filters &= Q(address__regency__icontains=entities['regency'])

    attribute_filter = Q()
    if 'attribute' in entities:
        attribute_filter = Q(name__icontains=entities['attribute']) | Q(
            description__icontains=entities['attribute'])

    if specific_filters:
        logger.debug(
            f"Menjalankan pencarian SPESIFIK dengan filter: {specific_filters}")
        results = base_queryset.filter(specific_filters)
        if attribute_filter:
            logger.debug(
                f"Menyaring hasil spesifik dengan atribut: {entities['attribute']}")
            results = results.filter(attribute_filter)

        if results.exists():
            logger.debug(
                f"Pencarian spesifik menemukan {results.count()} hasil.")
            return results.distinct().order_by('-average_rating')

    logger.debug("Menjalankan pencarian UMUM sebagai fallback.")
    general_filters = (
        Q(name__icontains=user_message) |
        Q(description__icontains=user_message) |
        # [REVISI] Gunakan 'categories' (jamak) untuk ManyToMany
        Q(categories__name__icontains=user_message)
    )
    if attribute_filter:
        general_filters |= attribute_filter

    results = base_queryset.filter(general_filters).distinct()
    logger.debug(f"Pencarian umum menemukan {results.count()} hasil.")
    return results.order_by('-average_rating')


def classify_user_intent(user_message: str) -> str:
    """Menggunakan LLM untuk mengklasifikasikan maksud utama pengguna."""
    if not gemini_model:
        return "SEARCH_QUERY"  # Default jika API error

    intent_prompt = f"""
        You are a high-speed intent classifier for a Bali tourism chatbot.
        Your only job is to classify the user's message into one of two categories:
        1. `SEARCH_QUERY`: If the message is about finding destinations, locations, prices, details, or recommendations related to tourism in Bali.
        2. `OFF_TOPIC`: If the message is a general knowledge question, a statement, or anything unrelated to Bali tourism.

        Respond with ONLY the category name.

        EXAMPLES:
        User Message: "rekomendasi pura di gianyar" -> Response: SEARCH_QUERY
        User Message: "berapa harga tiket ke uluwatu?" -> Response: SEARCH_QUERY
        User Message: "kenapa langit biru?" -> Response: OFF_TOPIC
        User Message: "ibu kota indonesia adalah" -> Response: OFF_TOPIC
        User Message: "thank you" -> Response: OFF_TOPIC
        
        ---
        Classify the following user message:
        User Message: "{user_message}"
        Response:
    """
    try:
        # Gunakan model yang sama, panggilannya akan sangat cepat untuk tugas ini
        classifier_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = classifier_model.generate_content(intent_prompt)
        intent = response.text.strip()
        logger.debug(f"Intent for '{user_message}' classified as: {intent}")
        if intent in ["SEARCH_QUERY", "OFF_TOPIC"]:
            return intent
        return "SEARCH_QUERY"  # Default jika respons tidak terduga
    except Exception:
        return "SEARCH_QUERY"  # Default jika ada error


def resolve_reference_with_gemini(history: list, user_message: str) -> str:
    """
    Menggunakan LLM untuk menyelesaikan referensi ambigu (seperti 'yang itu', 'yang pertama')
    menjadi nama entitas yang spesifik berdasarkan riwayat percakapan.
    """
    if not gemini_model:
        return "UNKNOWN"

    # Prompt yang sangat fokus pada satu tugas
    resolution_prompt = """
        You are a reference resolution model. Your task is to identify the specific destination name the user is referring to in their last message, based on the conversation history.
        - Analyze the history to understand the order of mentioned destinations.
        - Analyze the user's message for pronouns or references like 'the first one', 'that one', 'the temple', etc.
        - Respond ONLY with the full, exact name of the destination.
        - If you cannot determine the specific destination, respond with the single word: UNKNOWN.

        EXAMPLE 1:
        History: `[{'role': 'user', 'parts': ['pura di badung']}, {'role': 'model', 'parts': ['...Pura Luhur Uluwatu...']}, {'role': 'user', 'parts': ['pantai?']}, {'role': 'model', 'parts': ['...Pantai Kuta...']}]`
        User Message: "tell me about the first one"
        Response: Pura Luhur Uluwatu

        EXAMPLE 2:
        History: `[{'role': 'user', 'parts': ['pura di badung']}, {'role': 'model', 'parts': ['...Pura Luhur Uluwatu...']}]`
        User Message: "how much is the ticket?"
        Response: Pura Luhur Uluwatu

        EXAMPLE 3:
        History: `[{'role': 'user', 'parts': ['pura di badung']}, {'role': 'model', 'parts': ['...Pura Luhur Uluwatu...']}]`
        User Message: "thank you"
        Response: UNKNOWN
        
        ---
        """
    resolution_prompt += "CONVERSATION HISTORY:\n"
    resolution_prompt += str(history) + "\n\n"
    resolution_prompt += "USER MESSAGE:\n"
    resolution_prompt += f'"{user_message}"\n\n'
    resolution_prompt += "RESPONSE:\n"

    try:
        # Gunakan model yang sama, tapi tanpa history/system instruction yang mengganggu
        resolver_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = resolver_model.generate_content(resolution_prompt)
        resolved_name = response.text.strip()

        logger.debug(
            f"Reference resolution for '{user_message}' returned: '{resolved_name}'")

        if resolved_name == "UNKNOWN":
            return None
        return resolved_name
    except Exception as e:
        logger.error(f"Reference resolution failed: {e}")
        return None

# --- FUNGSI UTAMA (Sang Manajer) ---


def process_chatbot_message(user_message: str, session_id: str, user) -> str:
    if not gemini_model:
        return "Maaf, layanan chatbot sedang tidak tersedia saat ini."

    session, _ = ChatSession.objects.get_or_create(id=session_id)
    if user.is_authenticated and not session.user:
        session.user = user
        session.save()

    # Handle small talk
    normalized_message = user_message.lower().strip()
    if normalized_message in SMALL_TALK_RESPONSES:
        bot_reply = SMALL_TALK_RESPONSES[normalized_message]
        Message.objects.create(
            session=session, sender='user', text=user_message)
        Message.objects.create(session=session, sender='model', text=bot_reply)
        return bot_reply

    # Dapatkan riwayat chat untuk dikirim ke Gemini
    history_db = Message.objects.filter(
        session=session).order_by('-timestamp')[:6]
    formatted_history = [{'role': 'model' if msg.sender != 'user' else 'user', 'parts': [
        msg.text]} for msg in reversed(history_db)]

    rag_context = ""

    intent = classify_user_intent(user_message)

    if intent == 'OFF_TOPIC':
        logger.debug("Handling as OFF_TOPIC question.")
        rag_context = (
            "USER_IS_OFF_TOPIC. Your task is to politely decline the user's question because it is outside your expertise of Bali tourism. "
            "After declining, you MUST pivot the conversation back by suggesting specific topics you CAN help with. "
            "The ONLY allowed topics for suggestion are: 'pantai' (beaches), 'pura' (temples), 'air terjun' (waterfalls), and 'pengalaman budaya' (cultural experiences). "
            "Explicitly DO NOT suggest restaurants, hotels, shopping, or transportation."
        )
    else:
        # Proses utama
        entities = extract_entities(user_message)
        print(entities)
        active_context = session.active_context or {}
        has_active_context = 'destinations' in active_context and active_context[
            'destinations']

        is_explicit_new_search = 'category_slug' in entities or 'regency' in entities

        is_very_general_query = not entities and 'bali' in user_message.lower()

        # [REVISI] Struktur if/else dibalik (Inversi Logika)
        if has_active_context and not is_explicit_new_search:
            # --- BLOK 1: INI ADALAH PERTANYAAN LANJUTAN ---
            logger.debug(
                f"Menangani '{user_message}' sebagai PERTANYAAN LANJUTAN.")

            mentioned_name = resolve_reference_with_gemini(
                formatted_history, user_message)

            # Jika tidak ada nama spesifik disebut, gunakan konteks yang ada
            if not mentioned_name:
                logger.debug(
                    "Referensi tidak terdeteksi, menggunakan konteks aktif terakhir.")
                rag_context = "Ini adalah pertanyaan lanjutan tentang konteks terakhir:\n"

                destinations_in_context = active_context.get(
                    'destinations', [])

                # Buat konteks yang kaya agar Gemini bisa menjawab pertanyaan perbandingan
                for dest in destinations_in_context:
                    rag_context += (
                        f"- Nama: {dest.get('name', 'N/A')}, "
                        f"Lokasi: {dest.get('full_address', 'N/A')}, "
                        f"Rating: {dest.get('average_rating', 'N/A')}, "
                        f"Harga Tiket: {dest.get('ticket_price_range', 'N/A')}, "
                        f"Deskripsi Singkat: {dest.get('description_snippet', 'N/A')}...\n"
                    )
            else:
                logger.debug(
                    f"Pengguna menyebut nama spesifik: {mentioned_name}. Melakukan pencarian targeted.")
                # Panggil fungsi dengan target_name
                results = get_rag_context_from_db(
                    {}, "", target_name=mentioned_name)

                if results.exists():
                    logger.debug(
                        f"Pencarian targeted untuk '{mentioned_name}' berhasil.")
                    rag_context, context_to_save = _format_results_and_build_context(
                        results,
                        headline="Tentu, ini informasi lebih detail tentang yang kamu tanyakan:\n",
                        limit=1  # Cukup ambil satu hasil yang paling relevan
                    )
                    session.active_context = {'destinations': context_to_save}
                    session.save()
                else:
                    # Jika pencarian targeted gagal, baru kita katakan tidak ada.
                    logger.debug(
                        f"Pencarian targeted untuk '{mentioned_name}' gagal.")
                    rag_context = f"DATABASE_RESULT: NOT_FOUND for {mentioned_name}, lalu jelaskan bahwa informasi spesifik tentang itu tidak ditemukan di database Balinara."
        elif is_very_general_query:
            # --- [BLOK BARU] BLOK 2: MENANGANI PERMINTAAN UMUM "TOP HITS" ---
            logger.debug(
                f"Menangani '{user_message}' sebagai PERMINTAAN UMUM.")

            # Lakukan query sederhana untuk mendapatkan 3 destinasi dengan rating tertinggi
            results = Destination.objects.filter(
                is_published=True).order_by('-average_rating')[:3]

            if results.exists():
                rag_context, context_to_save = _format_results_and_build_context(
                    results,
                    headline="Tentu! Bali punya banyak sekali tempat indah. Berikut adalah beberapa rekomendasi terpopuler:\n"
                )
                session.active_context = {'destinations': context_to_save}
                session.save()
            else:
                # Fallback jika ternyata database benar-benar kosong
                rag_context = "DATABASE_RESULT: NOT_FOUND, lalu jelaskan bahwa belum ada destinasi di database."
                session.active_context = {}
                session.save()
        else:
            logger.debug(f"Menangani '{user_message}' sebagai PENCARIAN BARU.")

            results = get_rag_context_from_db(entities, user_message)
            if results.exists():
                rag_context, context_to_save = _format_results_and_build_context(
                    results,
                    headline="Berikut data relevan dari database Balinara:\n"
                )
                session.active_context = {'destinations': context_to_save}
                session.save()
            else:
                rag_context = "DATABASE_RESULT: NOT_FOUND, lalu Ajak pengguna untuk menambahkan destinasi atau review baru di website Balinara."

    # [REVISI] Gunakan satu instance model saja, mulai chat baru dengan history
    chat_session = gemini_model.start_chat(history=formatted_history)

    prompt_with_context = f"""
SYSTEM_INSTRUCTION:
---
{FINAL_RESPONSE_SYSTEM_INSTRUCTION}
---

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
        logger.error(f"Error during final response generation: {e}")
        bot_response_text = "Maaf, saya sedikit bingung. Bisa coba tanyakan dengan cara lain?"

    # Simpan pesan ke database
    Message.objects.create(session=session, sender='user', text=user_message)
    Message.objects.create(
        session=session, sender='model', text=bot_response_text)
    return bot_response_text


def _format_results_and_build_context(results: QuerySet, headline: str, limit: int = 3) -> tuple[str, list]:
    """
    Fungsi helper untuk memformat QuerySet menjadi RAG context dan context untuk disimpan di sesi.
    Ini untuk menghindari duplikasi kode.
    """
    rag_context = headline
    context_to_save = []

    for dest in results[:limit]:
        category_names = ", ".join(
            [cat.name for cat in dest.categories.all()]) or "N/A"
        full_address = dest.address.get_full_address() if dest.address else 'N/A'

        rag_context += (
            f"- **{dest.name}**\n"
            f"  Lokasi: {full_address}\n"
            f"  Kategori: {category_names}\n"
            f"  Rating: {dest.average_rating}\n"
            f"  Harga Tiket: {dest.ticket_price_range or '-'}\n"
            f"  Deskripsi: {dest.description[:120]}...\n\n"
        )

        latitude = dest.address.latitude if dest.address else None
        longitude = dest.address.longitude if dest.address else None
        context_to_save.append({
            'name': dest.name,
            'average_rating': float(dest.average_rating),
            'ticket_price_range': dest.ticket_price_range,
            'description_snippet': dest.description[:100],
            'full_address': full_address,
            'latitude': str(latitude) if latitude else None,
            'longitude': str(longitude) if longitude else None,
        })
    return rag_context, context_to_save


def process_image_query(image_file, user_message: str, session_id: str, user) -> str:
    """
    Memproses permintaan yang berisi gambar, menganalisisnya dengan Gemini,
    dan mencari hasilnya di database lokal.
    """
    logger.debug(f"Memulai analisis gambar untuk sesi {session_id}")
    if not gemini_model:
        return "Maaf, layanan analisis gambar sedang tidak tersedia."

    session, _ = ChatSession.objects.get_or_create(id=session_id)

    try:
        try:
            image_bytes = image_file.read()
            original_image = Image.open(io.BytesIO(image_bytes))
        except Exception as img_e:
            logger.error(f"Gagal memproses gambar: {img_e}")
            return "Maaf, terjadi masalah saat memproses gambar Anda. Pastikan format file didukung."

        MAX_SIZE = (1024, 1024)
        original_image.thumbnail(MAX_SIZE, Image.Resampling.LANCZOS)
        compressed_buffer = io.BytesIO()
        original_image.save(compressed_buffer, format='WEBP', quality=85)
        compressed_buffer.seek(0)
        img_for_gemini = Image.open(compressed_buffer)
        logger.debug(
            "Gambar berhasil dikompres ke format WEBP dan di-resize.")
        # --- Langkah 2: Buat Prompt Multimodal ---
        prompt_text = (
            "Analyze this image. Your task is to identify if it's a known tourist destination in Bali, Indonesia. "
            "Focus on landmarks, architectural styles, natural features (beaches, waterfalls), or specific signage. "
            "If you can identify a specific destination, respond with ONLY the exact name of that destination (e.g., 'Pura Tanah Lot', 'Tegalalang Rice Terrace')."
            "If you cannot confidently identify a specific Bali destination, respond with the single word: UNKNOWN."
        )

        # Jika pengguna mengirim teks bersama gambar, tambahkan sebagai petunjuk
        if user_message:
            prompt_text += f"\n\nAdditional context from user: '{user_message}'"

        # Gabungkan instruksi teks dan objek gambar menjadi satu prompt
        prompt_parts = [prompt_text, img_for_gemini]

        # --- Langkah 3: Panggil Gemini API ---
        logger.debug("Mengirim gambar ke Gemini untuk analisis...")
        response = gemini_model.generate_content(prompt_parts)
        destination_name = response.text.strip()
        logger.debug(f"Gemini mengidentifikasi sebagai: '{destination_name}'")

        bot_reply = ""
        if destination_name and destination_name != "UNKNOWN":
            # --- Langkah 4: Cari Hasil Analisis di Database Lokal ---
            # Kita gunakan lagi fungsi get_rag_context_from_db yang sudah pintar!
            results = get_rag_context_from_db(
                {}, "", target_name=destination_name)

            if results.exists():
                # --- Langkah 5: Format Respons Jika Ditemukan ---
                headline = f"Saya cukup yakin gambar ini adalah **{results.first().name}**! Berikut beberapa detailnya:\n"
                rag_context, context_to_save = _format_results_and_build_context(
                    results, headline=headline, limit=1)

                bot_reply = rag_context
                session.active_context = {'destinations': context_to_save}
                session.save()
            else:
                # Dikenali oleh Gemini, tapi tidak ada di database kita
                bot_reply = f"Menarik! Sepertinya saya mengenali ini sebagai {destination_name}, tapi sayangnya detailnya belum ada di database Balinara. Mungkin ini destinasi baru yang bisa kamu tambahkan?"
        else:
            # --- Langkah 6: Respons Jika Tidak Dikenali ---
            bot_reply = "Hmm, saya sudah coba menganalisis gambarnya tapi sepertinya saya belum mengenali tempat ini sebagai destinasi wisata di Bali. Mungkin Anda bisa coba gambar lain yang lebih jelas?"

    except Exception as e:
        logger.error(f"Error processing image query: {e}")
        bot_reply = "Maaf, terjadi sedikit masalah saat saya mencoba menganalisis gambar Anda. Silakan coba lagi."

    # --- Langkah 7: Simpan Percakapan ---
    # Kita representasikan pesan pengguna sebagai teks untuk disimpan di riwayat
    user_message_for_db = f"[Gambar Diupload] {user_message}".strip()
    image_file.seek(0)
    Message.objects.create(session=session, sender='user',
                           text=user_message_for_db, image=image_file)
    Message.objects.create(session=session, sender='model', text=bot_reply)

    return bot_reply
