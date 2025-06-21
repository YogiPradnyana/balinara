// src/stores/chatStore.js
import { defineStore } from 'pinia'
import apiClient from '@/api/axiosInstance' // Gunakan apiClient yang sudah ada

const CHAT_API_PATH = '/chat/' // Path relatif terhadap baseURL di apiClient

export const useChatStore = defineStore('chat', {
  state: () => ({
    sessionId: null, // Untuk menyimpan "Nomor Tiket" sesi
    messages: [],
    isSendingMessage: false,
    isLoadingHistory: false,
    error: null,
  }),

  getters: {
    // getters Anda sudah bagus, tidak perlu diubah
    getMessages: (state) => state.messages,
    isChatSending: (state) => state.isSendingMessage,
    isHistoryLoading: (state) => state.isLoadingHistory,
    chatError: (state) => state.error,
  },

  actions: {
    startSession() {
      let storedSessionId = sessionStorage.getItem('balinaraChatSessionId')
      if (storedSessionId) {
        this.sessionId = storedSessionId
      } else {
        this.sessionId = crypto.randomUUID()
        sessionStorage.setItem('balinaraChatSessionId', this.sessionId)
      }
    },

    // 2. Action untuk mengambil riwayat chat berdasarkan sesi
    async fetchHistory() {
      if (!this.sessionId) return

      this.isLoadingHistory = true
      this.error = null
      try {
        // Panggil endpoint history yang baru
        const response = await apiClient.get(`/chat/history/${this.sessionId}/`)
        this.messages = Array.isArray(response.data) ? response.data : []
      } catch (err) {
        console.error('Error fetching history:', err)
        this.error = 'Gagal memuat riwayat obrolan.'
      } finally {
        this.isLoadingHistory = false
      }
    },

    // 3. Action untuk mengirim pesan (sekarang sudah session-aware)
    async sendMessage(messageText) {
      if (!messageText.trim() || !this.sessionId) return

      this.isSendingMessage = true
      this.error = null

      // Optimistic UI: langsung tampilkan pesan user
      this.messages.push({
        sender: 'user',
        text: messageText,
        timestamp: new Date().toISOString(),
      })

      try {
        // Kirim request ke endpoint 'send' dengan menyertakan session_id
        const response = await apiClient.post('/chat/send/', {
          message: messageText,
          session_id: this.sessionId,
        })

        // Tambahkan balasan dari bot
        this.messages.push({
          sender: 'model',
          text: response.data.reply,
          timestamp: new Date().toISOString(),
        })
      } catch (err) {
        console.error('Error sending message:', err)
        this.error =
          err.response?.data?.error || 'Gagal mengirim pesan atau mendapatkan respons dari Bot.'
        // Tambahkan pesan error ke chat untuk feedback langsung
        this.messages.push({
          sender: 'model',
          text: `Maaf, terjadi kesalahan: ${this.error}`,
          timestamp: new Date().toISOString(),
        })
        throw new Error(this.error)
      } finally {
        this.isSendingMessage = false
      }
    },

    // 4. Action untuk mereset sesi di frontend (aman)
    clearSession() {
      this.messages = []
      this.sessionId = null
      sessionStorage.removeItem('balinaraChatSessionId')
      this.startSession() // Langsung mulai sesi baru yang bersih
    },
  },
})
