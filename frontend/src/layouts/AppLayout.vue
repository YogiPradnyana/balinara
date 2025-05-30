<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import { RouterView, useRoute } from 'vue-router'
import { onMounted, watch } from 'vue'
import Nara from '@/components/Nara.vue'

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
    <div class="relative font-pr text-neu-900 overflow-x-hidden">
      <RouterView :key="$route.fullPath" />
    </div>
    <Footer />
    <Nara />
  </div>
</template>
