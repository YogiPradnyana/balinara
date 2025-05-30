<script setup>
import LoginModal from './auth/LoginModal.vue'
import Exit from './icons/Exit.vue'
import HamburgerMenu from './icons/HamburgerMenu.vue'
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
  import('flowbite').then(({ initDropdowns }) => {
    initDropdowns() // Inisialisasi ulang dropdown
  })
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
    class="fixed top-0 left-0 w-9/12 h-full flex flex-col p-4 justify-between rounded-r-2xl bg-white z-64 transform transition-transform duration-500 ease-in-out sm:hidden"
    :class="isSidebarOpen ? 'translate-x-0' : '-translate-x-full'"
  >
    <div>
      <div class="w-full flex justify-end">
        <Exit @click="isSidebarOpen = false" />
      </div>
      <div class="px-2 mt-4 flex flex-col gap-4 font-pr">
        <!-- <div class="gap-3 flex items-center">
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
        </div> -->
        <h1 class="text-2xl md:text-3xl font-se font-semibold leading-[38px]">
          Bali<span class="text-pr-500">nara</span>
        </h1>

        <div class="bg-neu-100 h-[1px] w-full"></div>
        <ul class="flex flex-col font-medium text-neu-700 gap-4">
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
    class="px-6 sm:px-12 lg:px-[100px] font-pr border-b-[1.6px] border-neu-100 sm:border-none"
  >
    <div
      class="sm:px-4 lg:px-10 py-4 flex justify-between items-center sm:border-b-[1.6px] sm:border-neu-100"
    >
      <!-- Burger Icon (Mobile) -->
      <div class="sm:hidden">
        <button @click="toggleSidebar" aria-label="Toggle sidebar">
          <HamburgerMenu class="size-5" />
        </button>
      </div>
      <RouterLink
        :to="{ name: 'Home' }"
        class="text-2xl md:text-3xl font-se font-semibold leading-[38px]"
      >
        Bali<span class="text-pr-500">nara</span>
      </RouterLink>

      <!-- Nav Items (Desktop) -->
      <ul class="hidden sm:flex sm:gap-8 lg:gap-[60px] items-center font-medium text-neu-700">
        <li class="flex flex-col items-center justify-center group">
          <RouterLink
            :to="{ name: 'Destinations' }"
            class="transition-all duration-400 ease-in-out group-hover:text-pr-500"
            :class="$route.name === 'Destinations' ? ' text-pr-500' : ''"
            >Discover</RouterLink
          >
          <span
            class="w-0 h-[1.6px] bg-pr-500 rounded-full relative top-2 transition-all duration-500 ease-in-out group-hover:w-6"
            :class="$route.name === 'Destinations' ? ' w-6' : ''"
          ></span>
        </li>
        <li
          id="dropdownDefaultButton"
          data-dropdown-toggle="dropdown1"
          data-dropdown-trigger="click"
          data-dropdown-placement="bottom-start"
          class="cursor-pointer flex flex-col items-center justify-center group"
        >
          <span class="transition-all duration-400 ease-in-out group-hover:text-pr-500"
            >Review</span
          >
          <span
            class="w-0 h-[1.6px] bg-pr-500 rounded-full relative top-2 transition-all duration-500 ease-in-out group-hover:w-6"
          ></span>
        </li>

        <!-- Dropdown menu -->
        <div id="dropdown1" class="z-50 hidden bg-sur-50 rounded-2xl p-2 shadow-md">
          <ul class="flex flex-col gap-2" aria-labelledby="dropdownHoverButton">
            <li>
              <RouterLink
                :to="{ name: 'WriteReview' }"
                class="block rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                >Write a review</RouterLink
              >
            </li>
            <li>
              <RouterLink
                :to="{ name: 'SuggestSpot' }"
                class="block rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                >Suggest a spot</RouterLink
              >
            </li>
          </ul>
        </div>

        <li class="flex flex-col items-center justify-center group">
          <RouterLink
            :to="{ name: 'About' }"
            class="transition-all duration-400 ease-in-out group-hover:text-pr-500"
            :class="$route.name === 'About' ? ' text-pr-500' : ''"
            >About</RouterLink
          >
          <span
            class="w-0 h-[1.6px] bg-pr-500 rounded-full relative top-2 transition-all duration-500 ease-in-out group-hover:w-6"
            :class="$route.name === 'About' ? ' w-6' : ''"
          ></span>
        </li>
      </ul>

      <!-- Sign In (Desktop) -->
      <div
        class="hidden cursor-pointer sm:flex px-4.5 py-2.5 gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
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
      'fixed top-0 left-0 right-0 z-50 transition-all duration-500 font-pr bg-white px-6 sm:px-12 lg:px-[100px] border-b-[1.6px] border-neu-100 sm:border-none',
      isSticky ? 'translate-y-0 opacity-100' : '-translate-y-40 opacity-0',
    ]"
  >
    <div
      class="sm:px-2 lg:px-10 py-4 flex justify-between gap-8 sm:gap-4 items-center sm:border-b-[1.6px] sm:border-neu-100"
    >
      <div class="sm:hidden">
        <button @click="toggleSidebar" aria-label="Toggle sidebar">
          <HamburgerMenu class="size-5" />
        </button>
      </div>

      <form
        class="flex sm:max-w-[560px] sm:order-2 w-full items-center justify-between rounded-full outline outline-neu-200 p-1"
      >
        <div class="wrapper gap-2 ps-1.5 flex items-center w-full">
          <Search class="min-w-5" />
          <input
            type="text"
            class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
            placeholder="Type something here..."
          />
        </div>
        <button
          type="submit"
          class="px-4 md:px-6 py-1.5 flex text-sm lg:text-base gap-2 items-center justify-center font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
        >
          Search
        </button>
      </form>
      <RouterLink
        :to="{ name: 'Home' }"
        class="text-xl sm:order-1 md:text-2xl lg:text-3xl font-se font-semibold"
      >
        Bali<span class="text-pr-500">nara</span>
      </RouterLink>
      <ul
        class="hidden sm:order-3 sm:flex text-base sm:text-sm lg:text-base gap-4 lg:gap-8 xl:gap-[60px] items-center font-medium text-neu-700"
      >
        <li class="flex flex-col items-center justify-center group">
          <RouterLink
            :to="{ name: 'Destinations' }"
            class="transition-all duration-400 ease-in-out group-hover:text-pr-500"
            :class="$route.name === 'Destinations' ? ' text-pr-500' : ''"
            >Discover</RouterLink
          >
          <span
            class="w-0 h-[1.6px] bg-pr-500 rounded-full relative top-2 transition-all duration-500 ease-in-out group-hover:w-6"
            :class="$route.name === 'Destinations' ? ' w-6' : ''"
          ></span>
        </li>
        <li
          id="dropdownDefaultButton"
          data-dropdown-toggle="dropdown2"
          data-dropdown-trigger="click"
          data-dropdown-placement="bottom-start"
          class="cursor-pointer flex flex-col items-center justify-center group"
        >
          <span
            class="transition-all flex items-center gap-0.5 duration-400 ease-in-out group-hover:text-pr-500"
            >Review</span
          >
          <span
            class="w-0 h-[1.6px] bg-pr-500 rounded-full relative top-2 transition-all duration-500 ease-in-out group-hover:w-6"
          ></span>
        </li>

        <!-- Dropdown menu -->
        <div id="dropdown2" class="z-50 hidden bg-sur-50 rounded-2xl p-2 shadow-md">
          <ul class="flex flex-col gap-2" aria-labelledby="dropdownHoverButton">
            <li>
              <RouterLink
                :to="{ name: 'WriteReview' }"
                class="block rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                >Write a review</RouterLink
              >
            </li>
            <li>
              <RouterLink
                :to="{ name: 'SuggestSpot' }"
                class="block rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                >Suggest a spot</RouterLink
              >
            </li>
          </ul>
        </div>

        <li class="flex flex-col items-center justify-center group">
          <RouterLink
            :to="{ name: 'About' }"
            class="transition-all duration-400 ease-in-out group-hover:text-pr-500"
            :class="$route.name === 'About' ? ' text-pr-500' : ''"
            >About</RouterLink
          >
          <span
            class="w-0 h-[1.6px] bg-pr-500 rounded-full relative top-2 transition-all duration-500 ease-in-out group-hover:w-6"
            :class="$route.name === 'About' ? ' w-6' : ''"
          ></span>
        </li>
      </ul>

      <div
        class="hidden sm:order-4 whitespace-nowrap sm:flex px-4.5 py-2.5 text-sm lg:text-base gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
        @click="isLoginOpen = true"
      >
        <Login class="hidden lg:flex" />
        Sign in
      </div>
    </div>
  </nav>

  <LoginModal v-if="isLoginOpen" @close="isLoginOpen = false" />
  <!-- <LoginEmailModal /> -->
  <!-- <RegisterEmailModal /> -->
</template>

<style scoped>
/* Optional smooth scroll fix for Safari */
html {
  scroll-behavior: smooth;
}
</style>
