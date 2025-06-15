import { defineStore } from 'pinia'
import apiClient from '@/api/axiosInstance'

const CATEGORIES_API_PATH = '/common/categories/'

export const useCategoryStore = defineStore('category', {
  state: () => ({
    categories: [], // Array untuk menyimpan daftar kategori
    currentCategory: null, // Untuk menyimpan kategori yang sedang dilihat/diedit
    isLoading: false,
    error: null, // Untuk menyimpan pesan error
    pagination: {
      count: 0,
      next: null,
      previous: null,
    },
  }),

  getters: {
    allCategories: (state) => state.categories,
    getCategoryById: (state) => (id) => state.categories.find((cat) => cat.id === id),
    isLoadingCategories: (state) => state.isLoading,
    categoryError: (state) => state.error,
  },

  actions: {
    async fetchCategories(params = {}) {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.get(CATEGORIES_API_PATH, { params })
        // Jika API Anda menggunakan paginasi DRF standar:
        if (response.data && typeof response.data.results !== 'undefined') {
          this.categories = response.data.results
          this.pagination.count = response.data.count
          this.pagination.next = response.data.next
          this.pagination.previous = response.data.previous
        } else {
          // Jika API mengembalikan array langsung (tanpa paginasi wrapper)
          this.categories = Array.isArray(response.data) ? response.data : []
          // Reset paginasi jika tidak ada
          this.pagination = { count: this.categories.length, next: null, previous: null }
        }
      } catch (err) {
        console.error('Error fetching categories:', err)
        this.error =
          err.response?.data?.detail ||
          err.response?.data ||
          err.message ||
          'Failed to fetch categories.'
        this.categories = [] // Kosongkan jika error
      } finally {
        this.isLoading = false
      }
    },

    async fetchCategory(idOrSlug) {
      // Untuk mengambil satu kategori
      this.isLoading = true
      this.error = null
      this.currentCategory = null
      try {
        const response = await apiClient.get(`${CATEGORIES_API_PATH}${idOrSlug}/`)
        this.currentCategory = response.data
      } catch (err) {
        console.error(`Error fetching category ${idOrSlug}:`, err)
        this.error =
          err.response?.data?.detail ||
          err.response?.data ||
          err.message ||
          'Failed to fetch category details.'
      } finally {
        this.isLoading = false
      }
    },

    async createCategory(categoryData) {
      // categoryData adalah objek { name, description? }
      this.isLoading = true
      this.error = null
      try {
        // apiClient akan otomatis menambahkan token jika endpoint ini memerlukannya
        const response = await apiClient.post(CATEGORIES_API_PATH, categoryData)
        // Tambahkan kategori baru ke state lokal setelah berhasil dibuat di server
        this.categories.push(response.data)
        // Atau panggil fetchCategories lagi untuk data yang paling update, tapi kurang efisien
        // await this.fetchCategories();
        return response.data // Kembalikan data kategori baru
      } catch (err) {
        console.error('Error creating category:', err)
        this.error = err.response?.data || err.message || 'Failed to create category.'
        throw this.error // Lempar error agar komponen bisa menanganinya (misal, menampilkan error validasi)
      } finally {
        this.isLoading = false
      }
    },

    async updateCategory(idOrSlug, categoryData) {
      this.isLoading = true
      this.error = null
      try {
        const response = await apiClient.put(`${CATEGORIES_API_PATH}${idOrSlug}/`, categoryData) // atau .patch()
        // // Update kategori di state lokal
        // const index = this.categories.findIndex((cat) => cat.id === response.data.id)
        // if (index !== -1) {
        //   this.categories[index] = response.data
        // }
        // if (this.currentCategory && this.currentCategory.id === response.data.id) {
        //   this.currentCategory = response.data
        // }
        await this.fetchCategories() // Alternatif: fetch ulang semua
        return response.data
      } catch (err) {
        console.error(`Error updating category ${idOrSlug}:`, err)
        this.error = err.response?.data || err.message || 'Failed to update category.'
        throw this.error
      } finally {
        this.isLoading = false
      }
    },

    async deleteCategory(idOrSlug) {
      this.isLoading = true
      this.error = null
      try {
        await apiClient.delete(`${CATEGORIES_API_PATH}${idOrSlug}/`)
        // Hapus kategori dari state lokal
        this.categories = this.categories.filter(
          (cat) => cat.id !== idOrSlug && cat.slug !== idOrSlug,
        )
        if (
          this.currentCategory &&
          (this.currentCategory.id === idOrSlug || this.currentCategory.slug === idOrSlug)
        ) {
          this.currentCategory = null
        }
        // await this.fetchCategories(); // Alternatif: fetch ulang semua
      } catch (err) {
        console.error(`Error deleting category ${idOrSlug}:`, err)
        this.error =
          err.response?.data?.detail ||
          err.response?.data ||
          err.message ||
          'Failed to delete category.'
        throw this.error
      } finally {
        this.isLoading = false
      }
    },

    // Fungsi untuk membersihkan error jika diperlukan
    clearError() {
      this.error = null
    },
  },
})
