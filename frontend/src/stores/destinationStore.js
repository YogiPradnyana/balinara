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
        console.log(response.data)
      } catch (err) {
        /* ... handle error ... */
      } finally {
        this.isLoadingDetail = false
      }
    },

    async uploadTemporaryImage(file) {
      const formData = new FormData()
      formData.append('image', file)

      try {
        // Panggil endpoint temp-images yang baru dibuat
        const response = await apiClient.post(`${DESTINATIONS_API_PATH}temp-images/`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        return response.data // Mengembalikan data gambar sementara {id, image, ...}
      } catch (err) {
        console.error('Temporary Image Upload Error:', err.response?.data)
        // Lemparkan error agar bisa ditangani di komponen
        throw err.response?.data || { detail: 'Failed to upload temporary image.' }
      }
    },

    async createDestination(destinationData) {
      this.isLoadingDetail = true
      this.error = null

      try {
        const response = await apiClient.post(DESTINATIONS_API_PATH, destinationData, {
          headers: {
            // Pastikan header di-set ke JSON, karena kita tidak mengirim file langsung di sini
            'Content-Type': 'application/json',
          },
        })

        await this.fetchDestinations()

        return response.data
      } catch (err) {
        this.error = err.response?.data || { general: 'Gagal membuat destinasi.' }
        console.error('Create Destination Error:', this.error)
        throw err
      } finally {
        this.isLoadingDetail = false
      }
    },

    async updateDestination(slug, destinationData) {
      this.isLoadingDetail = true
      this.error = null

      try {
        // Gunakan PATCH untuk mengirim hanya data yang berubah

        const response = await apiClient.patch(`${DESTINATIONS_API_PATH}${slug}/`, destinationData)

        // Update data di state jika sedang dilihat
        this.currentDestination = response.data

        // Muat ulang daftar untuk konsistensi
        await this.fetchDestinations()

        return response.data
      } catch (err) {
        this.error = err.response?.data || { general: 'Gagal mengupdate destinasi.' }
        console.error('Update Destination Error:', this.error)
        throw err
      } finally {
        this.isLoadingDetail = false
      }
    },

    async deleteDestination(slug) {
      // Gunakan isLoadingDetail karena kita beroperasi pada satu item
      this.isLoadingDetail = true
      this.error = null

      try {
        // Kirim request DELETE ke backend
        await apiClient.delete(`${DESTINATIONS_API_PATH}${slug}/`)

        // PENTING: Setelah berhasil menghapus, panggil ulang fetchDestinations
        // agar data di halaman daftar destinasi menjadi ter-update.
        await this.fetchDestinations({ page: this.pagination.currentPage })

        // Jika Anda sedang berada di halaman detail yang dihapus,
        // Anda bisa membersihkan state-nya
        if (this.currentDestination && this.currentDestination.slug === slug) {
          this.currentDestination = null
        }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Gagal menghapus destinasi.'
        console.error(this.error)
      } finally {
        this.isLoadingDetail = false
      }
    },

    async uploadDestinationImage(slug, formData) {
      this.error = null

      try {
        const response = await apiClient.post(`/destinations/${slug}/images/upload/`, formData, {
          headers: {
            'Content-Type': undefined,
          },
        })

        const newImages = response.data.uploaded_images

        // 1. Pastikan respons berisi data yang kita harapkan
        if (newImages && this.currentDestination && this.currentDestination.images) {
          // 2. Tambahkan gambar-gambar baru ke array yang sudah ada (Mutasi Lokal)
          this.currentDestination.images.push(...newImages)
        }

        return response.data
      } catch (err) {
        console.error('Upload Image Error in Store:', err.response?.data)
        this.error =
          err.response?.data?.detail ||
          err.response?.data?.errors?.join(', ') ||
          'An error occurred during image upload.'
        throw this.error
      }
    },

    async deleteDestinationImage(slug, imageId) {
      this.error = null

      try {
        // Kirim request DELETE ke URL custom action untuk menghapus gambar.
        // Perhatikan bagaimana kita menyusun URL-nya sesuai dengan yang ada di views.py Anda.
        await apiClient.delete(`${DESTINATIONS_API_PATH}${slug}/images/${imageId}/delete/`)

        // Sama seperti upload, setelah berhasil hapus, muat ulang data destinasi
        // agar gambar yang dihapus hilang dari tampilan.
        if (this.currentDestination && this.currentDestination.images) {
          // 2. Buat array baru tanpa gambar yang dihapus (Mutasi Lokal)
          this.currentDestination.images = this.currentDestination.images.filter(
            (image) => image.id !== imageId,
          )
        }
      } catch (err) {
        this.error = err.response?.data?.detail || 'Gagal menghapus gambar.'
        console.error('Delete Image Error:', this.error)
        throw err
      }
    },

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
