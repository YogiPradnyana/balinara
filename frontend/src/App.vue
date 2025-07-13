<script setup>
import { RouterView } from 'vue-router'
import { Toaster } from 'vue-sonner'
import 'vue-sonner/style.css'

// --- PERUBAHAN DIMULAI DI SINI ---
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import { useUiStore } from '@/stores/uiStore'
import VueEasyLightbox from 'vue-easy-lightbox'

const uiStore = useUiStore()

const isLightboxVisible = computed(() => uiStore.isLightboxVisible)
const lightboxImages = computed(() => uiStore.lightboxImages)
const lightboxIndex = computed(() => uiStore.lightboxIndex)
// Inisialisasi auth store
const authStore = useAuthStore()

// Saat komponen App pertama kali dimuat (setelah refresh atau kunjungan pertama),
// jalankan fungsi untuk memeriksa status otentikasi dari localStorage.
onMounted(() => {
  authStore.checkAuthStatus()
})
// --- AKHIR DARI PERUBAHAN ---
</script>

<template>
  <div class="antialiased">
    <Toaster position="top-right" :expand="true" />
    <VueEasyLightbox
      :visible="isLightboxVisible"
      :imgs="lightboxImages"
      :index="lightboxIndex"
      @hide="uiStore.closeLightbox"
    />
    <RouterView :key="$route.fullPath" />
  </div>
</template>

<style>
/* ... style global Anda yang lain ... */

/* === KUSTOMISASI VUE-SONNER === */
[data-sonner-toast][data-type='success'] [data-icon] {
  color: #5cce74;
}
[data-sonner-toast][data-type='error'] [data-icon] {
  color: #f87171;
}
[data-sonner-toast][data-type='info'] [data-icon] {
  color: #60a5fa;
}
[data-t-warning] [data-icon] {
  color: #facc15;
}
</style>
