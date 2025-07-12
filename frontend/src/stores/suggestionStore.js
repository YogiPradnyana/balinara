import { defineStore } from 'pinia';

// 1. Impor instance axios terpusat Anda
import apiClient from '@/api/axiosInstance';

// 2. Definisikan path API sebagai konstanta agar mudah diubah
const SUGGESTIONS_API_PATH = '/suggestions/';

export const useSuggestionStore = defineStore('suggestion', {
  // Store ini tidak perlu 'state' atau 'getters' karena hanya bertugas mengirim data.
  // Semua data form dikelola secara lokal di dalam komponen SuggestSpot.vue.

  // 3. 'Actions' berisi semua fungsi yang bisa dipanggil dari komponen
  actions: {
    /**
     * Mengirim data suggestion baru ke backend.
     * @param {FormData} formData - Objek FormData yang berisi semua isian form, termasuk file.
     * @returns {Promise} - Mengembalikan promise dari panggilan API.
     */
    createSuggestion(formData) {
      // Mengirim request POST ke alamat: /api/suggestions/
      // Header 'Content-Type': 'multipart/form-data' penting untuk upload file.
      return apiClient.post(SUGGESTIONS_API_PATH, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
    },
  },
});