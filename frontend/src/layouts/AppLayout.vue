<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { RouterView, useRoute } from 'vue-router'
import { onMounted, watch } from 'vue'
import Nara from '@/components/Nara.vue'
import LoginModal from '@/components/auth/LoginModal.vue'
import { useAuthStore } from '@/stores/authStore'
import { Toaster, toast } from 'vue-sonner'
import 'vue-sonner/style.css'

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
  <Toaster position="top-right" theme="light" />
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

<style>
/* ... style global Anda yang lain ... */

/* === KUSTOMISASI VUE-SONNER === */

/* Menargetkan semua ikon di dalam toast sukses */
/* Atribut [data-type="success"] akan muncul jika Anda menggunakan `richColors` */
[data-sonner-toast][data-type='success'] [data-icon] {
  color: #5cce74; /* Ganti dengan warna hijau yang Anda inginkan, misal: Tailwind's Emerald 400 */
}

/* Menargetkan semua ikon di dalam toast error */
[data-sonner-toast][data-type='error'] [data-icon] {
  color: #f87171; /* Ganti dengan warna merah yang Anda inginkan, misal: Tailwind's Red 400 */
}

/* Menargetkan semua ikon di dalam toast info */
[data-sonner-toast][data-type='info'] [data-icon] {
  color: #60a5fa; /* Ganti dengan warna biru yang Anda inginkan */
}

/* Menargetkan semua ikon di dalam toast warning */
[data-sonner-toast][data-t-warning] [data-icon] {
  color: #facc15; /* Ganti dengan warna kuning yang Anda inginkan */
}

/* Jika Anda TIDAK menggunakan `richColors`, selector-nya sedikit berbeda */
/* Gunakan ini jika Anda tidak memakai `richColors` */
/*
[data-sonner-toast] .success [data-icon] {
  color: green;
}
[data-sonner-toast] .error [data-icon] {
  color: red;
}
*/
</style>
