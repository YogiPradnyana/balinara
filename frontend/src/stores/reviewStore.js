// frontend/src/stores/reviewStore.js

import { defineStore } from 'pinia'
import apiClient from '@/api/axiosInstance'

export const useReviewStore = defineStore('review', {
  state: () => ({
    reviews: [],
    isLoading: false,
    error: null,
  }),
  actions: {
    // Action untuk mengambil semua review untuk satu destinasi
    async fetchReviewsByDestination(destinationId) {
      if (!destinationId) return
      this.isLoading = true
      this.error = null
      try {
        // API akan memfilter berdasarkan destination_id yang dikirim sebagai query param
        const response = await apiClient.get('/reviews/', {
          params: { destination_id: destinationId },
        })
        this.reviews = response.data
      } catch (err) {
        this.error = err
        console.error('Failed to fetch reviews:', err)
      } finally {
        this.isLoading = false
      }
    },

    // Action untuk membuat review baru
    async createReview(reviewData) {
      // Tidak perlu set isLoading karena user akan di-redirect
      this.error = null
      try {
        // Kirim data { destination, rating, comment } ke backend
        const response = await apiClient.post('/reviews/', reviewData)
        return response.data
      } catch (err) {
        console.error('Failed to create review:', err.response.data)
        // Lemparkan error agar bisa ditangkap oleh komponen
        throw err
      }
    },
  },
})
