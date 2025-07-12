import { defineStore } from 'pinia';
import suggestionService from '@/services/suggestionService'; // Menggunakan service yang sudah dibuat

export const useSuggestionStore = defineStore('suggestion', {
  state: () => ({
    mySuggestions: [], // Untuk menyimpan daftar saran milik user
    isLoading: false,
    error: null,
  }),
  getters: {
    allMySuggestions: (state) => state.mySuggestions,
  },
  actions: {
    /**
     * Mengambil riwayat saran dari API dan menyimpannya ke state.
     */
    async fetchMySuggestions() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await suggestionService.getMySuggestions();
        
        // =================================================================
        // PERUBAHAN KUNCI ADA DI SINI
        // DRF mengirim data dalam format paginasi, jadi kita ambil array dari 'results'.
        // =================================================================
        this.mySuggestions = response.data.results;

      } catch (err) {
        this.error = err.response?.data || 'Failed to fetch suggestions.';
        console.error("Error fetching my suggestions:", err);
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Membuat suggestion baru melalui service.
     * @param {FormData} formData
     */
    async createSuggestion(formData) {
      // Fungsi ini hanya melempar promise, loading/error dihandle di komponen
      try {
        const response = await suggestionService.create(formData);
        // Setelah berhasil membuat, kita bisa langsung tambahkan ke daftar
        // agar UI terupdate tanpa perlu refresh halaman.
        if (response.data) {
          this.mySuggestions.unshift(response.data); // unshift() menambah ke awal array
        }
        return response;
      } catch (error) {
        // Lemparkan error agar komponen form bisa menanganinya
        throw error;
      }
    },
  },
});
