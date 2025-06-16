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
  },

  actions: {
    // _updateFacilityInState(updatedFacility) {
    //   const index = this.facilities.findIndex((fac) => fac.id === updatedFacility.id)
    //   if (index !== -1) {
    //     this.facilities[index] = updatedFacility
    //   } else {
    //     // Jika tidak ditemukan (misal setelah create lalu langsung edit tanpa fetch ulang),
    //     // tambahkan ke daftar jika belum ada (meskipun create seharusnya sudah menambahkannya)
    //     // atau panggil fetchFacilities lagi. Untuk update, biasanya sudah ada.
    //     this.facilities.push(updatedFacility) // Atau handle berbeda
    //   }
    // },

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

    async fetchFacility(idOrSlug) {
      // Untuk mengambil satu kategori
      this.isLoading = true
      this.error = null
      this.currentFacility = null
      try {
        const response = await apiClient.get(`${FACILITIES_API_PATH}${idOrSlug}/`)
        this.currentFacility = response.data
      } catch (err) {
        console.error(`Error fetching facility ${idOrSlug}:`, err)
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

    async updateFacility(idOrSlug, facilityData) {
      // { name, icon_url? }
      this.isLoading = true
      this.error = null
      try {
        // Gunakan PUT atau PATCH. PUT biasanya mengganti seluruh resource.
        // PATCH hanya field yang dikirim. Serializer Anda harus mendukungnya.
        const response = await apiClient.put(`${FACILITIES_API_PATH}${idOrSlug}/`, facilityData)
        await this.fetchFacilities()
        return response.data
      } catch (err) {
        this.error = err.response?.data || err.message || 'Failed to update facility.'
        console.error(`Error updating facility ${idOrSlug}:`, err)
        throw this.error
      } finally {
        this.isLoading = false
      }
    },

    async deleteFacility(idOrSlug) {
      this.isLoading = true
      this.error = null
      try {
        await apiClient.delete(`${FACILITIES_API_PATH}${idOrSlug}/`)
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
