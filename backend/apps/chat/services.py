# apps/chat/services.py

import google.generativeai as genai
import json
import logging
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
    "If the context says 'DATABASE_RESULT: NOT_FOUND', you MUST politely inform the user that you couldn't find a matching destination and then warmly invite them to contribute to Balinara by adding a new destination or review on the website. "
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
        safety_settings=safety_settings,
        # [REVISI] Definisikan system instruction sekali saja
        system_instruction=FINAL_RESPONSE_SYSTEM_INSTRUCTION
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

    # Proses utama
    entities = extract_entities(user_message)
    active_context = session.active_context or {}
    has_active_context = 'destinations' in active_context and active_context['destinations']

    # [BARU] Cek apakah pengguna secara eksplisit meminta pencarian baru
    is_explicit_new_search = 'category_slug' in entities or 'regency' in entities

    rag_context = ""

    # [REVISI] Struktur if/else dibalik (Inversi Logika)
    if has_active_context and not is_explicit_new_search:
        # --- BLOK 1: INI ADALAH PERTANYAAN LANJUTAN ---
        logger.debug(
            f"Menangani '{user_message}' sebagai PERTANYAAN LANJUTAN.")

        mentioned_name = entities.get('attribute') or entities.get(
            'destination_name')  # Asumsi NLU bisa ekstrak 'destination_name'

        # Jika tidak ada nama spesifik disebut, gunakan konteks yang ada
        if not mentioned_name:
            rag_context = "Ini adalah pertanyaan lanjutan. Konteks dari percakapan sebelumnya adalah tentang destinasi berikut:\n"
            destinations_in_context = active_context.get('destinations', [])

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
                # Jika ditemukan, perlakukan sebagai "pencarian baru" yang sukses
                # dan perbarui konteks aktif.
                logger.debug(
                    f"Pencarian targeted untuk '{mentioned_name}' berhasil.")
                # (Kita bisa duplikasi sedikit kode dari blok 'else' untuk memformat hasil)
                rag_context = "Tentu, ini informasi lebih detail tentang yang kamu tanyakan:\n"
                context_to_save = []  # Siapkan untuk memperbarui konteks
                for dest in results[:1]:  # Ambil satu yang paling relevan
                    category_names = ", ".join(
                        [cat.name for cat in dest.categories.all()]) or "N/A"
                    full_address = dest.address.get_full_address() if dest.address else 'N/A'
                    rag_context += (
                        f"- Nama: {dest.name}, "
                        f"Lokasi: {full_address}, "
                        f"Kategori: {category_names}, "
                        f"Rating: {dest.average_rating}, "
                        f"Harga Tiket: {dest.ticket_price_range or '-'}.\n"
                        f"Deskripsi: {dest.description}\n"
                    )
                    context_to_save.append({
                        'name': dest.name,
                        'average_rating': float(dest.average_rating),
                        'ticket_price_range': dest.ticket_price_range,
                        'description_snippet': dest.description[:100],
                        'location': full_address
                    })
                session.active_context = {'destinations': context_to_save}
                session.save()
            else:
                # Jika pencarian targeted gagal, baru kita katakan tidak ada.
                logger.debug(
                    f"Pencarian targeted untuk '{mentioned_name}' gagal.")
                rag_context = f"DATABASE_RESULT: NOT_FOUND for {mentioned_name}, lalu jelaskan bahwa informasi spesifik tentang itu tidak ditemukan di database Balinara."

    else:
        # --- BLOK 2: INI ADALAH PENCARIAN BARU ---
        logger.debug(f"Menangani '{user_message}' sebagai PENCARIAN BARU.")

        results = get_rag_context_from_db(entities, user_message)
        if results.exists():
            rag_context = "Berikut data relevan dari database Balinara:\n"
            context_to_save = []
            for dest in results[:3]:
                category_names = ", ".join(
                    [cat.name for cat in dest.categories.all()]) or "N/A"
                full_address = dest.address.get_full_address() if dest.address else 'N/A'
                rag_context += (
                    f"- Nama: {dest.name}, "
                    f"Lokasi: {full_address}, "
                    f"Kategori: {category_names}, "
                    f"Rating: {dest.average_rating}, "
                    f"Harga Tiket: {dest.ticket_price_range or '-'}.\n"
                    f"Deskripsi: {dest.description[:100]}...\n"
                )
                context_to_save.append({
                    'name': dest.name,
                    'average_rating': float(dest.average_rating),
                    'ticket_price_range': dest.ticket_price_range,
                    'description_snippet': dest.description[:100],
                    'location': full_address
                })
            # Simpan konteks baru ke sesi
            session.active_context = {'destinations': context_to_save}
        else:
            rag_context = "DATABASE_RESULT: NOT_FOUND, lalu Ajak pengguna untuk menambahkan destinasi atau review baru di website Balinara."
            # Kosongkan konteks jika tidak ada hasil
            session.active_context = {}
        session.save()

    # Dapatkan riwayat chat untuk dikirim ke Gemini
    history_db = Message.objects.filter(
        session=session).order_by('-timestamp')[:6]
    formatted_history = [{'role': 'model' if msg.sender != 'user' else 'user', 'parts': [
        msg.text]} for msg in reversed(history_db)]

    # [REVISI] Gunakan satu instance model saja, mulai chat baru dengan history
    chat_session = gemini_model.start_chat(history=formatted_history)

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
        logger.error(f"Error during final response generation: {e}")
        bot_response_text = "Maaf, saya sedikit bingung. Bisa coba tanyakan dengan cara lain?"

    # Simpan pesan ke database
    Message.objects.create(session=session, sender='user', text=user_message)
    Message.objects.create(
        session=session, sender='model', text=bot_response_text)
    return bot_response_text
