<template>
  <div class="chat-container">
    <h2>🤖 Gemini Chatbot 🤖</h2>
    <div class="message-list" ref="messageList">
      <div v-if="messages.length === 0 && !error && !isLoadingHistory" class="no-messages">
        Mulai obrolan Anda dengan Gemini!
      </div>
      <div v-if="isLoadingHistory" class="loading-messages">
        Memuat riwayat obrolan...
      </div>
      <div v-for="message in messages" :key="message.id" 
           :class="['message-item', message.sender === 'user' ? 'user-message' : 'bot-message']">
        <strong>{{ message.sender === 'user' ? 'Anda' : 'Bot' }}:</strong> 
        <p v-html="formatMessage(message.text)"></p>
        <small>{{ new Date(message.timestamp).toLocaleTimeString() }}</small>
      </div>
    </div>
    <div class="message-input">
      <input 
        v-model="userMessage" 
        @keyup.enter="sendMessage" 
        placeholder="Ketik pesan Anda..." 
        class="input-field"
        :disabled="isSending"
      />
      <button @click="sendMessage" :disabled="isSending || !userMessage.trim()" class="send-button">
        {{ isSending ? 'Mengirim...' : 'Kirim' }}
      </button>
    </div>
    <button @click="clearHistory" class="clear-button" :disabled="isClearing">
      {{ isClearing ? 'Menghapus...' : 'Bersihkan Riwayat' }}
    </button>
    <p v-if="error" class="error-message">{{ error }}</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ChatGemini',
  data() {
    return {
      messages: [],
      userMessage: '',
      isSending: false,
      isClearing: false,
      isLoadingHistory: false,
      error: null,
      // *************************************************************************
      // PENTING: SESUAIKAN DENGAN URL API DJANGO ANDA!
      // Jika Django berjalan di http://localhost:8000 dan Anda meng-include 'chat.urls' di bawah '/api/'
      // maka URL-nya adalah 'http://localhost:8000/api/'
      // *************************************************************************
      djangoApiBaseUrl: 'http://localhost:8000/api/', 
    };
  },
  mounted() {
    this.fetchMessages();
  },
  updated() {
    this.scrollToBottom(); // Scroll ke bawah setiap kali pesan diperbarui
  },
  methods: {
    formatMessage(text) {
      // Mengganti baris baru (\n) dengan tag HTML <br> agar ditampilkan sebagai baris baru di HTML
      // Mengganti double asterisk (**) dengan bold tag HTML untuk format markdown sederhana
      // Mengganti single asterisk (*) dengan italic tag HTML
      if (!text) return '';
      let formattedText = text.replace(/\n/g, '<br>');
      formattedText = formattedText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>'); // Bold
      formattedText = formattedText.replace(/\*(.*?)\*/g, '<em>$1</em>'); // Italic
      return formattedText;
    },
    async fetchMessages() {
      this.error = null;
      this.isLoadingHistory = true;
      try {
        const response = await axios.get(`${this.djangoApiBaseUrl}messages/`);
        this.messages = response.data;
        this.scrollToBottom();
      } catch (err) {
        console.error('Error fetching messages:', err);
        this.error = 'Gagal memuat riwayat obrolan. Pastikan server Django berjalan dan konfigurasi CORS sudah benar.';
      } finally {
        this.isLoadingHistory = false;
      }
    },
    async sendMessage() {
      if (!this.userMessage.trim()) {
        this.error = 'Pesan tidak boleh kosong.';
        return;
      }
      this.isSending = true;
      this.error = null;

      const messageToSend = this.userMessage;
      this.userMessage = ''; // Hapus input segera untuk pengalaman pengguna yang lebih baik

      // Tambahkan pesan user ke daftar secara sementara sebelum respons bot datang (Optimistic UI)
      const tempUserMessage = {
        id: 'temp-' + Date.now(), // ID sementara untuk rendering
        sender: 'user',
        text: messageToSend,
        timestamp: new Date().toISOString()
      };
      this.messages.push(tempUserMessage);
      this.scrollToBottom();

      try {
        const response = await axios.post(`${this.djangoApiBaseUrl}chat/`, { 
          message: messageToSend 
        });

        // Hapus pesan user sementara dari daftar
        this.messages = this.messages.filter(msg => msg.id !== tempUserMessage.id);

        // Tambahkan pesan user dan respons bot yang sebenarnya dari API (data yang valid)
        this.messages.push(response.data.user_message);
        this.messages.push(response.data.bot_response);
        this.scrollToBottom();
      } catch (err) {
        console.error('Error sending message:', err.response ? err.response.data : err.message);
        this.error = 'Gagal mengirim pesan atau mendapatkan respons dari Bot. Coba lagi.';
        // Jika ada kesalahan, hapus pesan user sementara dari daftar
        this.messages = this.messages.filter(msg => msg.id !== tempUserMessage.id);
      } finally {
        this.isSending = false;
      }
    },
    async clearHistory() {
      if (!confirm('Apakah Anda yakin ingin menghapus seluruh riwayat obrolan? Tindakan ini tidak dapat dibatalkan.')) {
        return;
      }
      this.error = null;
      this.isClearing = true;
      try {
        await axios.post(`${this.djangoApiBaseUrl}clear_history/`);
        this.messages = []; // Kosongkan array pesan di frontend setelah berhasil dihapus di backend
        alert('Riwayat obrolan berhasil dihapus.');
      } catch (err) {
        console.error('Error clearing history:', err.response ? err.response.data : err.message);
        this.error = 'Gagal menghapus riwayat obrolan. Coba lagi.';
      } finally {
        this.isClearing = false;
      }
    },
    scrollToBottom() {
      // Fungsi untuk menggeser scroll ke bawah otomatis
      this.$nextTick(() => { // Menunggu DOM diperbarui
        const messageList = this.$refs.messageList;
        if (messageList) {
          messageList.scrollTop = messageList.scrollHeight;
        }
      });
    }
  }
};
</script>

<style scoped>
/* Styling bisa disesuaikan dengan tema proyek Vue Anda */
.chat-container {
  max-width: 700px;
  margin: 50px auto;
  padding: 25px;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 25px;
  font-size: 1.8em;
}

.message-list {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
}

.no-messages, .loading-messages {
    text-align: center;
    color: #888;
    padding: 20px;
    font-style: italic;
}
.loading-messages {
    color: #007bff;
}

.message-item {
  padding: 10px 15px;
  margin-bottom: 10px;
  border-radius: 15px;
  max-width: 80%;
  line-height: 1.5;
  font-size: 0.95em;
}

.user-message {
  background-color: #e6f7ff; /* Light blue */
  align-self: flex-end;
  text-align: right;
}

.bot-message {
  background-color: #e9ffe6; /* Light green */
  align-self: flex-start;
  text-align: left;
}

.message-item strong {
  display: block;
  margin-bottom: 5px;
  font-size: 0.85em;
  color: #555;
}
.user-message strong { color: #007bff; }
.bot-message strong { color: #28a745; }


.message-item p {
  margin: 0;
  word-wrap: break-word; /* Memastikan teks tidak keluar batas */
}

.message-item small {
  display: block;
  font-size: 0.7em;
  color: #999;
  margin-top: 5px;
}

.message-input {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.input-field {
  flex-grow: 1;
  padding: 12px 15px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 1em;
  outline: none;
  transition: border-color 0.3s;
}

.input-field:focus {
  border-color: #007bff;
}

.send-button {
  padding: 12px 25px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.send-button:hover:not(:disabled) {
  background-color: #0056b3;
}

.send-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.clear-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #dc3545; /* Red */
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9em;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}

.clear-button:hover:not(:disabled) {
  background-color: #c82333;
}
.clear-button:disabled {
    background-color: #cccccc;
    cursor: not-allowed;
}

.error-message {
  color: #dc3545;
  background-color: #f8d7da;
  border: 1px solid #f5c6cb;
  padding: 10px;
  border-radius: 5px;
  margin-top: 15px;
  text-align: center;
}
</style>