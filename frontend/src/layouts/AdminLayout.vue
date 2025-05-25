<script setup>
import { RouterView } from 'vue-router'
import Footer from '@/components/admin/Footer.vue'
import Header from '@/components/admin/Header.vue'
import Sidebar from '@/components/admin/Sidebar.vue'
import { ref } from 'vue'
const isSidebarOpen = ref(false)
</script>
<template>
  <div class="min-h-screen lg:flex font-pr text-neu-900">
    <!-- Backdrop for mobile sidebar -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-neu-900 opacity-50 z-60 lg:hidden"
      @click="isSidebarOpen = false"
    />
    <Sidebar :is-sidebar-open="isSidebarOpen" />
    <div class="flex-1 flex flex-col transition-all duration-300 ease-in-out lg:ml-64">
      <Header @sidebar-open="isSidebarOpen = !isSidebarOpen" :is-sidebar-open="isSidebarOpen" />
      <main class="p-6 flex-1 overflow-x-hidden">
        <RouterView />
      </main>
      <Footer />
    </div>
  </div>
</template>
