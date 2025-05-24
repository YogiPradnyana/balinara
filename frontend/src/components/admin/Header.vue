<script setup>
import ArrowDown from '@/components/icons/ArrowDown.vue'
import { ref } from 'vue'
import Home from '../icons/Home.vue'
import Users from '../icons/Users.vue'
import OutlinedLocation from '../icons/OutlinedLocation.vue'
import Tag from '../icons/Tag.vue'
import Message from '../icons/Message.vue'
import MapPin from '../icons/MapPin.vue'
const isSidebarOpen = ref(false)
const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}
</script>
<template>
  <!-- Backdrop for mobile sidebar -->
  <div
    v-if="isSidebarOpen"
    class="fixed inset-0 bg-neu-900 opacity-50 z-60"
    @click="isSidebarOpen = false"
  />

  <!-- Mobile Sidebar -->
  <aside
    class="fixed top-0 left-0 min-w-64 flex flex-col gap-10 p-4 min-h-screen bg-sur-50 border-r border-neu-200 z-64 transform transition-transform duration-500 ease-in-out lg:hidden"
    :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
  >
    <h1 class="text-2xl font-se font-semibold pl-3">Bali<span class="text-pr-500">nara</span></h1>
    <div class="space-y-4 text-sm">
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">Master</h3>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center text-pr-500 py-2 px-4 font-medium bg-[#EFF6F2] hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <Home class="text-pr-500 size-5" />Dashboard
        </RouterLink>
      </div>
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">User</h3>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <Users class="text-neu-500 size-5" />Management
        </RouterLink>
      </div>
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">Katalog</h3>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <OutlinedLocation class="text-neu-500 size-5" />Destinations
        </RouterLink>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <Tag class="text-neu-500 size-5" />Categories
        </RouterLink>
      </div>
      <div class="space-y-3">
        <h3 class="text-sm font-semibold uppercase text-neu-500 pl-3">REVIEWS</h3>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex gap-3 items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <Message class="text-neu-500 size-5" />Testimonials
        </RouterLink>
        <RouterLink
          :to="{ name: 'Wishlist' }"
          class="flex justify-between items-center py-2 px-4 font-medium hover:bg-[#EFF6F2] transition-all duration-50 rounded-xl"
        >
          <span class="flex items-center gap-3"
            ><MapPin class="text-neu-500 size-5" />Suggested Spot</span
          ><span
            class="flex items-center text-neu-50 text-sm rounded-[6px] justify-center px-2 bg-pr-500"
            >2</span
          >
        </RouterLink>
      </div>
    </div>
  </aside>

  <div
    class="flex justify-between lg:justify-end items-center px-6 py-3.5 bg-sur-50 border-b border-neu-200"
  >
    <div class="lg:hidden transform transition-transform duration-500 ease-in-out">
      <button @click="toggleSidebar" class="cursor-pointer" aria-label="Toggle sidebar">
        <svg
          class="w-6 h-6 text-gray-700"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    </div>
    <div class="gap-3 w-fit flex items-center">
      <img src="@/assets/images/User Avatar.jpg" alt="User Profile" class="size-9 rounded-full" />
      <p class="text-neu-900 gap-0.5 flex items-center font-medium text-sm max-w-36 line-clamp-1">
        <span class="hidden sm:block">Udin Surudin</span><ArrowDown class="text-neu-900" />
      </p>
    </div>
  </div>
</template>
