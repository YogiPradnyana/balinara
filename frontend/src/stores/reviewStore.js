// frontend/src/stores/reviewStore.js

import { defineStore } from 'pinia'
import apiClient from '@/api/axiosInstance'
import { useAuthStore } from './authStore'

export const useReviewStore = defineStore('review', {
  state: () => ({
    reviews: [],
    myReviews: [],
    currentReview: null,
    reviewSummary: {
      total_reviews: 0,
      average_rating: 0,
      rating_distribution: [],
    },
    pagination: {
      count: 0,
      next: null,
      previous: null,
    },
    isLoading: false,
    error: null,
  }),
  actions: {
    async fetchMyReviews() {
      const authStore = useAuthStore()
      if (!authStore.currentUser?.id) return // Jangan lakukan apa-apa jika user tidak login

      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get('/reviews/', {
          params: { user: authStore.currentUser.id }, // Kirim ID user sebagai parameter
        })
        // Karena endpoint ini menggunakan paginasi, data ada di dalam 'results'
        this.myReviews = response.data.results || []
        console.log(this.myReviews)
      } catch (err) {
        this.error = err
        console.error('Gagal mengambil ulasan saya:', err)
      } finally {
        this.isLoading = false
      }
    },

    async fetchAllReviews(params = {}) {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get('/reviews/', { params })
        this.reviews = response.data.results || []
        this.pagination = {
          count: response.data.count || 0,
          next: response.data.next,
          previous: response.data.previous,
        }
      } catch (err) {
        console.error('Failed to fetch all reviews:', err)
        this.error = err
      } finally {
        this.isLoading = false
      }
    },

    // Action untuk mengambil detail satu review berdasarkan ID
    async fetchReviewById(reviewId) {
      this.isLoading = true
      this.currentReview = null
      try {
        const response = await apiClient.get(`/reviews/${reviewId}/`)
        this.currentReview = response.data
      } catch (err) {
        console.error(`Failed to fetch review ${reviewId}:`, err)
        this.error = err
      } finally {
        this.isLoading = false
      }
    },

    // Action untuk menghapus review
    async deleteReview(reviewId) {
      try {
        await apiClient.delete(`/reviews/${reviewId}/`)
        // Hapus review dari state lokal agar UI langsung update tanpa refresh
        const index = this.reviews.findIndex((r) => r.id === reviewId)
        if (index > -1) {
          this.reviews.splice(index, 1)
          this.pagination.count-- // Kurangi jumlah total
        }
        showNotification('success', 'Review has been deleted successfully.')
      } catch (err) {
        showNotification('error', 'Failed to delete the review.')
        console.error(`Failed to delete review ${reviewId}:`, err)
      }
    },

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

    async fetchReviewsByDestination(destinationId, filters = {}) {
      if (!destinationId) return
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get('/reviews/', {
          params: { destination: destinationId, ...filters },
        })

        if (response.data) {
          this.reviews = response.data.results || response.data || []
          this.pagination.count = response.data.count || 0
          this.pagination.next = response.data.next || null
          this.pagination.previous = response.data.previous || null
          if (response.data.summary) {
            this.reviewSummary = response.data.summary || {}
          }
        } else {
          this.reviews = []
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
