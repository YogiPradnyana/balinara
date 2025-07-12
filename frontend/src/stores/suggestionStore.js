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
  }),
  getters: {
    allMySuggestions: (state) => state.mySuggestions,
    adminSuggestions: (state) => state.suggestionsList,
    suggestionDetail: (state) => state.currentSuggestion,
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
        }
        return response;
      } catch (error) {
        throw error;
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
        
        // =================================================================
        // PERUBAHAN KUNCI ADA DI SINI
        // Update state 'currentSuggestion' dengan data baru dari server.
        // =================================================================
        this.currentSuggestion = response.data;

        return response; // Kirim respons untuk notifikasi di komponen
      } catch (error) {
        console.error("Gagal update status:", error);
        throw error; // Lemparkan error agar komponen tahu ada kegagalan
      }
    },

    async deleteSuggestion(id, currentParams) {
      try {
        await suggestionService.delete(id);
        await this.fetchAdminSuggestions(currentParams);
      } catch (error) {
        throw error;
      }
    },
  },
});
