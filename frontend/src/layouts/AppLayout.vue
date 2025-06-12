<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { RouterView, useRoute } from 'vue-router'
import { onMounted, watch } from 'vue'
import Nara from '@/components/Nara.vue'
import LoginModal from '@/components/auth/LoginModal.vue'
import { useAuthStore } from '@/stores/authStore'

const authStore = useAuthStore()
// Lock scroll saat login dibuka
watch(authStore.showLoginModal, (val) => {
  if (val) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onMounted(() => {
  import('flowbite').then(({ initDropdowns }) => {
    initDropdowns() // Inisialisasi ulang dropdown
  })
})

watch(useRoute(), () => {
  import('flowbite').then(({ initDropdowns }) => {
    initDropdowns()
  })
})
</script>
<template>
  <div>
    <Navbar />
    <div class="relative min-h-screen font-pr text-neu-900 overflow-x-hidden">
      <RouterView :key="$route.fullPath" />
    </div>
    <Footer />
    <Nara />
    <LoginModal v-if="authStore.showLoginModal" @close="authStore.closeLoginModal()" />
  </div>
</template>
