<script setup>
import { RouterView } from 'vue-router'
import Footer from '@/components/admin/Footer.vue'
import Header from '@/components/admin/Header.vue'
import Sidebar from '@/components/admin/Sidebar.vue'
import { ref } from 'vue'
import ConfirmationModal from '@/components/modals/ConfirmationModal.vue'

const isSidebarOpen = ref(false)
</script>

<template>
  <div class="min-h-screen lg:flex font-pr text-neu-900">
    <!-- Backdrop for mobile sidebar -->
    <!-- PERUBAHAN: z-index diubah dari z-60 menjadi z-40 -->
    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-neu-900 opacity-50 z-40 lg:hidden"
      @click="isSidebarOpen = false"
    />
    <Sidebar :is-sidebar-open="isSidebarOpen" />
    <div class="flex-1 flex flex-col transition-all duration-300 ease-in-out lg:ml-64">
      <Header @sidebar-open="isSidebarOpen = !isSidebarOpen" :is-sidebar-open="isSidebarOpen" />
      <main class="p-6 flex-1 overflow-x-hidden">
        <RouterView :key="$route.fullPath" />
      </main>
      <Footer />
    </div>

    <!-- Komponen Modal Konfirmasi -->
    <!-- z-index di sini (z-50) sudah lebih tinggi dari backdrop sidebar (z-40) -->
    <ConfirmationModal />
  </div>
</template>
