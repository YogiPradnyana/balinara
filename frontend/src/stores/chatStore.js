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
    async sendMessage(payload) {
      const { text, image } = payload

      if (!this.sessionId) {
        console.error('Session ID is missing.')
        this.error = 'Session not started. Please refresh.'
        return
      }

      this.isSendingMessage = true
      this.error = null

      // Optimistic UI: langsung tampilkan pesan user
      const userMessage = {
        id: `temp-user-${Date.now()}`,
        sender: 'user',
        text: text,
        timestamp: new Date().toISOString(),
        // [BARU] Tambahkan representasi gambar untuk ditampilkan di UI jika ada
        image_url: image ? URL.createObjectURL(image) : null,
      }
      this.messages.push(userMessage)

      try {
        const formData = new FormData()
        formData.append('session_id', this.sessionId)
        if (text) {
          formData.append('message', text)
        }
        if (image) {
          formData.append('image', image)
        }

        const response = await apiClient.post(
          `/chat/send/`, // Atau endpoint baru Anda
          formData,
        )

        const botMessage = {
          id: `msg-${Date.now()}`,
          sender: 'model',
          text: response.data.reply,
          timestamp: new Date().toISOString(),
        }
        this.messages.push(botMessage)
      } catch (err) {
        console.error('Error sending message:', err)
        this.error =
          err.response?.data?.error || 'Gagal mengirim pesan atau mendapatkan respons dari Bot.'
        // Tambahkan pesan error ke chat untuk feedback langsung
        this.messages.push({
          id: `err-${Date.now()}`,
          sender: 'model',
          text: this.error,
          is_error: true,
        })
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
