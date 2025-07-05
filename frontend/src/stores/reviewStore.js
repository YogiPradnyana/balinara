// frontend/src/stores/reviewStore.js

import { defineStore } from 'pinia'
import apiClient from '@/api/axiosInstance'

export const useReviewStore = defineStore('review', {
  state: () => ({
    reviews: [],
    reviewSummary: {
      total_reviews: 0,
      average_rating: 0,
      rating_distribution: [],
    },
    isLoading: false,
    error: null,
  }),
  actions: {
    async uploadTemporaryReviewImage(file) {
      const formData = new FormData()
      formData.append('image', file)
      try {
        const response = await apiClient.post('/reviews/temp-images/', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })
        return response.data // Mengembalikan { id, image }
      } catch (err) {
        console.error('Temporary review image upload error:', err.response?.data)
        throw err.response?.data || { detail: 'Failed to upload image.' }
      }
    },

    async fetchReviewsByDestination(destinationId) {
      if (!destinationId) return
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get('/reviews/', {
          params: { destination_id: destinationId },
        })

        if (response.data) {
          this.reviews = response.data.reviews || []
          this.reviewSummary = response.data.summary || {}
        } else {
          this.reviews = []
          this.reviewSummary = {}
        }
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
