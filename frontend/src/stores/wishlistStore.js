// frontend/src/stores/wishlistStore.js

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/axiosInstance'

export const useWishlistStore = defineStore('wishlist', () => {
  // STATE: Daftar item wishlist
  const items = ref([])

  // GETTER (computed property) untuk pengecekan cepat
  const itemIds = computed(() => new Set(items.value.map((item) => item.destination.id)))

  // ACTIONS: Fungsi untuk memanipulasi state
  async function fetchWishlist() {
    try {
      // Logika API langsung di dalam action
      const response = await apiClient.get('/wishlists/')
      items.value = response.data.results || []
    } catch (error) {
      console.error('Gagal memuat wishlist:', error)
    }
  }

  async function add(destinationId) {
    if (isWishlisted(destinationId)) return // Hindari duplikasi
    try {
      // Logika API langsung di dalam action
      await apiClient.post('/wishlists/', { destination: destinationId })
      await fetchWishlist() // Ambil data terbaru untuk sinkronisasi penuh
    } catch (error) {
      console.error('Gagal menambah ke wishlist:', error)
      await fetchWishlist()
    }
  }

  async function remove(destinationId) {
    if (!isWishlisted(destinationId)) return
    try {
      // Logika API langsung di dalam action
      await apiClient.delete(`/wishlists/destinations/${destinationId}/`)
      // Update state lokal agar UI langsung reaktif
      await fetchWishlist()
    } catch (error) {
      console.error('Gagal menghapus dari wishlist:', error)
      await fetchWishlist()
    }
  }

  // Fungsi helper
  function isWishlisted(destinationId) {
    return itemIds.value.has(destinationId)
  }

  return { items, fetchWishlist, add, remove, isWishlisted }
})
