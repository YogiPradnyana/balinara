<script setup>
import { RouterLink, RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
  <header class="font-pr text-neu-900">
    <Navbar />
  </header>

  <div class="relative font-pr text-neu-900 overflow-hidden">
    <RouterView />
  </div>
</template>
