<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <Navbar />

  <div class="relative font-pr text-neu-900 overflow-x-hidden">
    <RouterView />
  </div>
  <Footer />
</template>
