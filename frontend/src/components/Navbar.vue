<script setup>
import Login from './icons/Login.vue'
import Search from './icons/Search.vue'
import { ref, onMounted, onUnmounted } from 'vue'

const isSticky = ref(false)
const isSidebarOpen = ref(false)

const handleScroll = () => {
  isSticky.value = window.scrollY > window.innerHeight
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})
onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}
</script>

<template>
  <!-- Backdrop for mobile sidebar -->
  <div
    v-if="isSidebarOpen"
    class="fixed inset-0 bg-neu-900 opacity-50 z-40 md:hidden"
    @click="isSidebarOpen = false"
  />

  <!-- Mobile Sidebar -->
  <aside
    class="fixed top-0 right-0 w-10/12 h-full rounded-l-3xl bg-white z-50 transform transition-transform duration-300 md:hidden"
    :class="isSidebarOpen ? 'translate-x-0' : 'translate-x-full'"
  >
    <div class="p-6 flex flex-col gap-6 font-pr">
      <h1 class="text-[32px] font-semibold leading-[38px]">
        Bali<span class="text-pr-500">nara</span>
      </h1>
      <ul class="flex flex-col gap-4 text-lg">
        <li>Discover</li>
        <li>Review</li>
        <li>About</li>
      </ul>
      <div
        class="mt-4 px-4.5 py-2.5 flex gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
      >
        <Login />
        Sign in
      </div>
    </div>
  </aside>

  <!-- Before Scroll Navbar (Desktop) -->
  <nav v-if="!isSticky" class="px-6 md:px-[100px] font-pr">
    <div
      class="px-4 md:px-10 py-4 flex justify-between items-center border-b-[1.6px] border-neu-100"
    >
      <h1 class="text-[32px] font-se font-semibold leading-[38px]">
        Bali<span class="text-pr-500">nara</span>
      </h1>

      <!-- Nav Items (Desktop) -->
      <ul class="hidden md:flex gap-[60px] items-center">
        <li>Discover</li>
        <li>Review</li>
        <li>About</li>
      </ul>

      <!-- Sign In (Desktop) -->
      <div
        class="hidden md:flex px-4.5 py-2.5 gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
      >
        <Login />
        Sign in
      </div>

      <!-- Burger Icon (Mobile) -->
      <div class="md:hidden">
        <button @click="toggleSidebar" aria-label="Toggle sidebar">
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
    </div>
  </nav>

  <!-- After Scroll Navbar (Sticky Top) -->
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-500 font-pr bg-white px-6 md:px-[100px]',
      isSticky ? 'translate-y-0 opacity-100' : '-translate-y-40 opacity-0',
    ]"
  >
    <div
      class="px-4 md:px-10 py-4 flex justify-between items-center border-b-[1.6px] border-neu-100"
    >
      <h1 class="text-[32px] font-se font-semibold leading-[38px]">
        Bali<span class="text-pr-500">nara</span>
      </h1>

      <form
        class="hidden md:flex max-w-[560px] w-full items-center justify-between rounded-full outline outline-neu-200 p-1"
      >
        <div class="wrapper gap-2 ps-1.5 flex items-center w-full">
          <Search />
          <input
            type="text"
            class="w-full text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
            placeholder="Type something here..."
          />
        </div>
        <button
          type="submit"
          class="px-6 py-1.5 flex gap-2 items-center justify-center font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
        >
          Search
        </button>
      </form>

      <ul class="hidden md:flex gap-[60px] items-center">
        <li>Discover</li>
        <li>Review</li>
        <li>About</li>
      </ul>

      <div
        class="hidden md:flex px-4.5 py-2.5 gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
      >
        <Login />
        Sign in
      </div>

      <!-- Burger Icon (Mobile) -->
      <div class="md:hidden">
        <button @click="toggleSidebar" aria-label="Toggle sidebar">
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
    </div>
  </nav>
</template>

<style scoped>
/* Optional smooth scroll fix for Safari */
html {
  scroll-behavior: smooth;
}
</style>
