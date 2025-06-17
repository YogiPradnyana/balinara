// src/stores/facilityStore.js
import { defineStore } from 'pinia'
import apiClient from '@/api/axiosInstance'

const FACILITIES_API_PATH = '/common/facilities/' // Path relatif

export const useFacilityStore = defineStore('facility', {
  state: () => ({
    facilities: [],
    currentCategory: null, // Untuk menyimpan kategori yang sedang dilihat/diedit
    isLoading: false,
    error: null,
    pagination: {
      count: 0,
      next: null,
      previous: null,
    },
  }),

  getters: {
    allFacilities: (state) => state.facilities,
    isLoadingFacilities: (state) => state.isLoading,
    facilityError: (state) => state.error,
    getFacilityById: (state) => (id) => state.facilities.find((fac) => fac.id === id),
    getFacilityBySlug: (state) => (slug) => state.facilities.find((fac) => fac.slug === slug),
  },

  actions: {
    async fetchFacilities(params = {}) {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get(FACILITIES_API_PATH, { params })
        if (response.data && typeof response.data.results !== 'undefined') {
          this.facilities = response.data.results
          this.pagination.count = response.data.count
          this.pagination.next = response.data.next
          this.pagination.previous = response.data.previous
        } else {
          this.facilities = Array.isArray(response.data) ? response.data : []
          this.pagination = { count: this.facilities.length, next: null, previous: null }
        }
      } catch (err) {
        this.error = err.response?.data || err.message || 'Failed to fetch facilities.'
        this.facilities = []
        console.error('Error fetching facilities:', err)
      } finally {
        this.isLoading = false
      }
    },

    async fetchFacility(slug) {
      // Untuk mengambil satu kategori
      this.isLoading = true
      this.error = null
      this.currentFacility = null
      try {
        const response = await apiClient.get(`${FACILITIES_API_PATH}${slug}/`)
        this.currentFacility = response.data
      } catch (err) {
        console.error(`Error fetching facility ${slug}:`, err)
        this.error =
          err.response?.data?.detail ||
          err.response?.data ||
          err.message ||
          'Failed to fetch facility details.'
      } finally {
        this.isLoading = false
      }
    },

    async createFacility(facilityData) {
      // console.log(facilityData)

      // { name, icon_url? }
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.post(FACILITIES_API_PATH, facilityData)
        // Optimistic update atau push data baru
        this.facilities.push(response.data)
        return response.data
      } catch (err) {
        this.error = err.response?.data || err.message || 'Failed to create facility.'
        console.error('Error creating facility:', err)
        throw this.error
      } finally {
        this.isLoading = false
      }
    },

    async updateFacility(slug, facilityData) {
      // { name, icon_url? }
      this.isLoading = true
      this.error = null
      try {
        // Gunakan PUT atau PATCH. PUT biasanya mengganti seluruh resource.
        // PATCH hanya field yang dikirim. Serializer Anda harus mendukungnya.
        const response = await apiClient.put(`${FACILITIES_API_PATH}${slug}/`, facilityData)
        await this.fetchFacilities()
        return response.data
      } catch (err) {
        this.error = err.response?.data || err.message || 'Failed to update facility.'
        console.error(`Error updating facility ${slug}:`, err)
        throw this.error
      } finally {
        this.isLoading = false
      }
    },

    async deleteFacility(slug) {
      this.isLoading = true
      this.error = null
      try {
        await apiClient.delete(`${FACILITIES_API_PATH}${slug}/`)
        await this.fetchFacilities()
      } catch (err) {
        this.error = err.response?.data?.detail || err.message || 'Failed to delete facility.'
        console.error(`Error deleting facility ${facilityId}:`, err)
        throw this.error
      } finally {
        this.isLoading = false
      }
    },

    clearError() {
      this.error = null
    },
  },
})
