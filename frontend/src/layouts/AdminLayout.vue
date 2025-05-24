<script setup>
import { RouterView } from 'vue-router'
import Footer from '@/components/admin/Footer.vue'
import Header from '@/components/admin/Header.vue'
import Sidebar from '@/components/admin/Sidebar.vue'
</script>
<template>
  <div class="flex max-h-screen overflow-hidden font-pr text-neu-900 relative">
    <Sidebar />
    <div class="flex-1 flex flex-col">
      <Header />
      <div class="flex-1 overflow-y-scroll">
        <RouterView />
        <Footer />
      </div>
    </div>
  </div>
</template>
