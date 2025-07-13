import { defineStore } from 'pinia';
import suggestionService from '@/services/suggestionService';

export const useSuggestionStore = defineStore('suggestion', {
  state: () => ({
    mySuggestions: [],
    suggestionsList: [],
    pagination: {},
    currentSuggestion: null,
    isLoading: false,
    error: null,
    // --- TAMBAH STATE BARU UNTUK JUMLAH PENDING DI SIDEBAR ---
    allSuggestionsForAdminCount: [], // Akan menyimpan semua suggestions untuk dihitung
  }),

  getters: {
    allMySuggestions: (state) => state.mySuggestions,
    adminSuggestions: (state) => state.suggestionsList,
    suggestionDetail: (state) => state.currentSuggestion,
    // --- TAMBAH GETTER BARU UNTUK AKSES DATA PENDING ---
    allSuggestionsForCounting: (state) => state.allSuggestionsForAdminCount,
  },

  actions: {
    async fetchMySuggestions() {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await suggestionService.getMySuggestions();
        this.mySuggestions = response.data.results;
      } catch (err) {
        this.error = err.response?.data || 'Gagal memuat riwayat saran.';
      } finally {
        this.isLoading = false;
      }
    },

    async createSuggestion(formData) {
      try {
        const response = await suggestionService.create(formData);
        if (response.data) {
          this.mySuggestions.unshift(response.data);
          // Opsional: Jika Anda ingin jumlah pending di sidebar langsung terupdate setelah create
          // this.fetchAllSuggestionsForAdminCount(); 
        }
        return response;
      } catch (error) {
        throw error;
      }
    },

    // --- TAMBAH ACTION BARU UNTUK MENGAMBIL SEMUA SUGGESTION KHUSUS UNTUK COUNTING ---
    async fetchAllSuggestionsForAdminCount() {
      // Tidak set isLoading global agar tidak mempengaruhi loading status utama
      // this.isLoading = true; 
      this.error = null; // Reset error spesifik untuk aksi ini jika diperlukan
      try {
        // Panggil endpoint yang sama dengan fetchAdminSuggestions, tapi tanpa pagination/limit
        // Anda mungkin perlu memastikan API Anda memiliki endpoint yang mengembalikan semua
        // atau memperbolehkan parameter `page_size=all` atau sejenisnya.
        // Asumsi: suggestionService.getAll() tanpa params akan mengembalikan semua,
        // atau setidaknya halaman pertama dengan cukup banyak data.
        // Idealnya, backend Anda memiliki endpoint khusus untuk total count pending.
        const response = await suggestionService.getAll({ status: 'pending', page_size: 9999 }); // Ambil semua yang pending
        this.allSuggestionsForAdminCount = response.data.results;
      } catch (err) {
        // Handle error, mungkin log saja atau set error spesifik
        console.error("Gagal memuat semua suggestion untuk hitungan:", err.response?.data || err.message);
        // this.error = 'Gagal memuat total hitungan suggestion.'; 
      } finally {
        // this.isLoading = false;
      }
    },

    async fetchAdminSuggestions(params = {}) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await suggestionService.getAll(params);
        this.suggestionsList = response.data.results;
        this.pagination = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
        };
        // Opsional: Setelah fetchAdminSuggestions utama, panggil juga untuk update hitungan sidebar
        // this.fetchAllSuggestionsForAdminCount();
      } catch (err) {
        this.error = err.response?.data || 'Gagal memuat daftar suggestion.';
      } finally {
        this.isLoading = false;
      }
    },

    async fetchSuggestionDetail(id) {
      this.isLoading = true;
      this.error = null;
      this.currentSuggestion = null;
      try {
        const response = await suggestionService.getById(id);
        this.currentSuggestion = response.data;
      } catch (err) {
        this.error = err.response?.data || 'Gagal memuat detail suggestion.';
      } finally {
        this.isLoading = false;
      }
    },

    /**
     * Mengupdate status suggestion.
     */
    async updateSuggestionStatus(id, newStatus) {
      try {
        const response = await suggestionService.update(id, { status: newStatus });
        
        // Update state 'currentSuggestion' dengan data baru dari server.
        this.currentSuggestion = response.data;

        // Setelah update status, perbarui juga data untuk hitungan pending di sidebar
        this.fetchAllSuggestionsForAdminCount(); 

        return response; // Kirim respons untuk notifikasi di komponen
      } catch (error) {
        console.error("Gagal update status:", error);
        throw error; // Lemparkan error agar komponen tahu ada kegagalan
      }
    },

    async deleteSuggestion(id, currentParams) {
      try {
        await suggestionService.delete(id);
        // Setelah delete, perbarui daftar admin dan hitungan sidebar
        await this.fetchAdminSuggestions(currentParams);
        await this.fetchAllSuggestionsForAdminCount(); // Perbarui hitungan sidebar
      } catch (error) {
        throw error;
      }
    },
  },
});