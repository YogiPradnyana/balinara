// src/stores/destinationStore.js
import { defineStore } from 'pinia'
import apiClient from '@/api/axiosInstance' // Menggunakan apiClient

const DESTINATIONS_API_PATH = '/destinations/' // Path relatif dari baseURL apiClient

export const useDestinationStore = defineStore('destination', {
  state: () => ({
    destinations: [], // Untuk daftar destinasi
    currentDestination: null, // Untuk detail destinasi yang sedang dilihat
    isLoadingList: false,
    isLoadingDetail: false,
    error: null,
    pagination: {
      count: 0,
      next: null,
      previous: null,
      currentPage: 1, // Kelola halaman saat ini
    },
    // Anda bisa menambahkan state untuk filter dan search term di sini
    // currentFilters: {},
    // currentSearchTerm: '',
  }),

  getters: {
    allDestinations: (state) => state.destinations,
    destinationDetail: (state) => state.currentDestination,
    // ... getter lain ...
  },

  actions: {
    async fetchDestinations(params = {}) {
      // params bisa berisi { page, search, category__slug, dll. }
      this.isLoadingList = true
      this.error = null
      // Selalu sertakan nomor halaman saat ini dari state jika tidak ada di params
      const queryParams = { page: this.pagination.currentPage, ...params }

      try {
        const response = await apiClient.get(DESTINATIONS_API_PATH, { params: queryParams })
        if (response.data && typeof response.data.results !== 'undefined') {
          this.destinations = response.data.results
          this.pagination.count = response.data.count
          this.pagination.next = response.data.next
          this.pagination.previous = response.data.previous
          // Update currentPage berdasarkan params atau dari respons jika ada
          console.log(this.destinations)

          if (queryParams.page) this.pagination.currentPage = queryParams.page
        } else {
          /* ... handle respons non-paginasi ... */
        }
      } catch (err) {
        /* ... handle error ... */
      } finally {
        this.isLoadingList = false
      }
    },

    async fetchDestinationBySlug(slug) {
      this.isLoadingDetail = true
      this.error = null
      this.currentDestination = null
      try {
        const response = await apiClient.get(`${DESTINATIONS_API_PATH}${slug}/`)
        this.currentDestination = response.data
      } catch (err) {
        /* ... handle error ... */
      } finally {
        this.isLoadingDetail = false
      }
    },

    // --- AKAN KITA IMPLEMENTASIKAN NANTI ---
    // async createDestination(destinationData) { /* ... */ },
    // async updateDestination(slug, destinationData) { /* ... */ },
    // async deleteDestination(slug) { /* ... */ },
    // async uploadDestinationImage(slug, imageData) { /* ... */ },
    // async deleteDestinationImage(slug, imageId) { /* ... */ },

    setCurrentPage(page) {
      if (
        page > 0 &&
        page <= Math.ceil(this.pagination.count / /*PAGE_SIZE DARI BACKEND atau konstanta*/ 10)
      ) {
        this.pagination.currentPage = page
        this.fetchDestinations() // Fetch ulang dengan halaman baru
      }
    },
    // ... action lain
  },
})
