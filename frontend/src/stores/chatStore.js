// src/stores/chatStore.js
import { defineStore } from 'pinia'
import apiClient from '@/api/axiosInstance' // Gunakan apiClient yang sudah ada

const CHAT_API_PATH = '/chat/' // Path relatif terhadap baseURL di apiClient

export const useChatStore = defineStore('chat', {
  state: () => ({
    messages: [], // Array untuk menyimpan objek pesan { id, sender, text, timestamp }
    isSendingMessage: false, // Status untuk pengiriman pesan
    isLoadingHistory: false, // Status untuk memuat riwayat
    isClearingHistory: false, // Status untuk menghapus riwayat
    error: null, // Pesan error umum untuk chat
    // suggestedReplies bisa juga disimpan di sini jika ingin dikelola secara global
    // suggestedReplies: [
    //   'Tourist attractions in Bali',
    //   'Recommended interesting places',
    //   'Cultural experiences',
    //   'Adventure activities',
    // ],
  }),

  getters: {
    getMessages: (state) => state.messages,
    isChatSending: (state) => state.isSendingMessage,
    isHistoryLoading: (state) => state.isLoadingHistory,
    isHistoryClearing: (state) => state.isClearingHistory,
    chatError: (state) => state.error,
    // getSuggestedReplies: (state) => state.suggestedReplies,
  },

  actions: {
    // Helper untuk menambahkan pesan ke state
    _addMessage(message) {
      this.messages.push(message)
    },

    // Helper untuk menghapus pesan berdasarkan ID (misal, pesan sementara)
    _removeMessageById(messageId) {
      this.messages = this.messages.filter((msg) => msg.id !== messageId)
    },

    async fetchMessages() {
      this.isLoadingHistory = true
      this.error = null
      try {
        // apiClient akan otomatis menambahkan token jika ada (berguna jika riwayat chat nantinya butuh auth)
        const response = await apiClient.get(CHAT_API_PATH + 'messages/')
        this.messages = Array.isArray(response.data) ? response.data : []
      } catch (err) {
        console.error('Error fetching messages from store:', err)
        this.error =
          err.response?.data?.error || err.response?.data?.detail || 'Gagal memuat riwayat obrolan.'
        this.messages = [] // Kosongkan pesan jika gagal load
      } finally {
        this.isLoadingHistory = false
      }
    },

    async sendMessage(messageText) {
      if (!messageText.trim()) {
        this.error = 'Pesan tidak boleh kosong.'
        return // Jangan kirim jika kosong
      }
      this.isSendingMessage = true
      this.error = null

      const tempUserMessageId = 'temp-user-' + Date.now()
      this._addMessage({
        id: tempUserMessageId,
        sender: 'user',
        text: messageText,
        timestamp: new Date().toISOString(),
      })

      try {
        const response = await apiClient.post(CHAT_API_PATH, {
          message: messageText,
        })

        this._removeMessageById(tempUserMessageId) // Hapus pesan sementara

        if (response.data.user_message) {
          this._addMessage(response.data.user_message)
        }
        if (response.data.bot_response) {
          this._addMessage(response.data.bot_response)
        }
        // Logika untuk suggested replies bisa di-handle di komponen atau di sini
        // jika ingin store yang mengelolanya.
        return response.data // Kembalikan data jika komponen perlu info tambahan
      } catch (err) {
        console.error('Error sending message from store:', err)
        this.error =
          err.response?.data?.error ||
          err.response?.data?.detail ||
          'Gagal mengirim pesan atau mendapatkan respons dari Bot.'
        this._removeMessageById(tempUserMessageId) // Hapus pesan sementara jika error
        throw this.error // Lempar error agar komponen bisa menangkapnya jika perlu
      } finally {
        this.isSendingMessage = false
      }
    },

    async clearChatHistory() {
      // Tidak perlu konfirmasi di sini, komponen bisa menanganinya
      this.isClearingHistory = true
      this.error = null
      try {
        await apiClient.post(CHAT_API_PATH + 'clear_history/') // Sesuaikan jika methodnya DELETE
        this.messages = [] // Kosongkan messages di frontend
        // Logika untuk suggested replies bisa di-reset di sini atau di komponen
      } catch (err) {
        console.error('Error clearing history from store:', err)
        this.error =
          err.response?.data?.error ||
          err.response?.data?.detail ||
          'Gagal menghapus riwayat obrolan.'
        throw this.error
      } finally {
        this.isClearingHistory = false
      }
    },
  },
})
