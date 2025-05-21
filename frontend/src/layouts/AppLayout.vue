<script setup>
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>
<template>
  <div>
    <Navbar />
    <div class="relative font-pr text-neu-900 overflow-x-hidden">
      <router-view />
    </div>
    <Footer />
  </div>
</template>
