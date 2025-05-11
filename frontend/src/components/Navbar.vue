<script setup>
import LoginCard from './auth/LoginCard.vue'
import Exit from './icons/Exit.vue'
import Login from './icons/Login.vue'
import Search from './icons/Search.vue'
import { ref, onMounted, onUnmounted, watch } from 'vue'
const isLoginOpen = ref(false)

// Lock scroll saat login dibuka
watch(isLoginOpen, (val) => {
  if (val) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

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
    class="fixed inset-0 bg-neu-900 opacity-50 z-60 md:hidden"
    @click="isSidebarOpen = false"
  />

  <!-- Mobile Sidebar -->
  <aside
    class="fixed top-0 left-0 w-9/12 h-full flex flex-col p-4 justify-between rounded-r-2xl bg-white z-64 transform transition-transform duration-300 md:hidden"
    :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
  >
    <div>
      <div class="w-full flex justify-end">
        <Exit @click="isSidebarOpen = false" />
      </div>
      <div class="px-2 mt-4 flex flex-col gap-4 font-pr">
        <div class="gap-3 flex items-center">
          <img
            src="@/assets/images/User Avatar.jpg"
            alt="User Profile"
            class="size-12 rounded-full"
          />
          <div class="flex-col flex w-full">
            <p class="text-neu-600 text-sm">Hello,</p>
            <p class="text-neu-900 font-medium whitespace-nowrap max-w-36 line-clamp-1">
              Udin Surudin
            </p>
          </div>
        </div>

        <div class="bg-neu-100 h-[1px] w-full"></div>
        <ul class="flex flex-col text-neu-800 gap-4">
          <li>Discover</li>
          <li>Review</li>
          <li>About</li>
        </ul>
      </div>
    </div>
    <div class="px-2">
      <div
        class="px-4.5 py-2.5 flex gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
      >
        <Login />
        Sign in
      </div>
    </div>
  </aside>

  <!-- Before Scroll Navbar (Desktop) -->
  <nav
    v-if="!isSticky"
    class="px-6 md:px-[100px] font-pr border-b-[1.6px] border-neu-100 md:border-none"
  >
    <div
      class="md:px-10 py-4 flex justify-between items-center md:border-b-[1.6px] md:border-neu-100"
    >
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
      <h1 class="text-2xl md:text-3xl font-se font-semibold leading-[38px]">
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
        class="hidden cursor-pointer md:flex px-4.5 py-2.5 gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
        @click="isLoginOpen = true"
      >
        <Login />
        Sign in
      </div>
    </div>
  </nav>

  <!-- After Scroll Navbar (Sticky Top) -->
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-500 font-pr bg-white px-6 md:px-[100px] border-b-[1.6px] border-neu-100 md:border-none',
      isSticky ? 'translate-y-0 opacity-100' : '-translate-y-40 opacity-0',
    ]"
  >
    <div
      class="md:px-10 py-4 flex justify-between gap-4 md:gap-0 items-center md:border-b-[1.6px] md:border-neu-100"
    >
      <div class="flex items-center gap-1">
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
        <h1 class="text-xl md:text-3xl font-se font-semibold leading-[38px]">
          Bali<span class="text-pr-500">nara</span>
        </h1>
      </div>

      <form
        class="flex md:max-w-[560px] w-full items-center justify-between rounded-full outline outline-neu-200 p-1"
      >
        <div class="wrapper gap-2 ps-1.5 flex items-center w-full">
          <Search class="size-7 md:size-5" />
          <input
            type="text"
            class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
            placeholder="Type something here..."
          />
        </div>
        <button
          type="submit"
          class="px-4 md:px-6 py-1.5 flex gap-2 items-center justify-center font-medium leading-6 text-sm md:text-[16px] bg-pr-500 rounded-full text-neu-50"
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
        @click="isLoginOpen = true"
      >
        <Login />
        Sign in
      </div>
    </div>
  </nav>

  <LoginCard v-if="isLoginOpen" @close="isLoginOpen = false" />
</template>

<style scoped>
/* Optional smooth scroll fix for Safari */
html {
  scroll-behavior: smooth;
}
</style>
