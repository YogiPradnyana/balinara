<script setup>
import LoginModal from './auth/LoginModal.vue'
import Exit from './icons/Exit.vue'
import HamburgerMenu from './icons/HamburgerMenu.vue'
import defaultAvatar from '@/assets/images/user_profile/default-avatar.png'
import Login from './icons/Login.vue'
import Search from './icons/Search.vue'
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useAuthStore } from '@/stores/authStore'

const handleImageError = (event) => {
  event.target.src = defaultAvatar
}

const isLoginOpen = ref(false)

const authStore = useAuthStore()
// Lock scroll saat login dibuka
watch(isLoginOpen, (val) => {
  if (val) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

const isSticky = ref(false)
const isReviewOpen = ref(false)
const isSidebarOpen = ref(false)
const isUserOpen = ref(false)
const navbarRef = ref(null)
const navHeight = ref(0)
const isScrolled = ref(false)

const toggleReviewDropdown = () => {
  isReviewOpen.value = !isReviewOpen.value
}
const toggleUserDropdown = () => {
  isUserOpen.value = !isUserOpen.value
}

const handleScroll = () => {
  isScrolled.value = window.scrollY > navbarRef.value.offsetHeight
  isSticky.value = window.scrollY > window.innerHeight
}

onMounted(() => {
  nextTick(() => {
    if (navbarRef.value) {
      navHeight.value = navbarRef.value.offsetHeight
    }
  })
  window.addEventListener('click', (event) => {
    if (!event.target.closest('.reviews-dropdown')) {
      isReviewOpen.value = false
    }

    if (!event.target.closest('.user-dropdown')) {
      isUserOpen.value = false
    }
  })
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

  <div v-show="isSticky" :style="{ height: navHeight + 'px' }"></div>

  <!-- 
  SATU-SATUNYA Navbar.
  Kita menggunakan :class untuk mengubah segalanya secara dinamis.
-->
  <nav
    ref="navbarRef"
    :class="[
      'font-pr z-50',
      isSticky
        ? 'fixed top-0 transition-all duration-500 left-0 right-0 translate-y-0 opacity-100 bg-white'
        : 'relative', // State sebelum scroll
      // Class padding ini sama untuk kedua state
      'sm:px-12 lg:px-[100px]',
      isScrolled ? '-translate-y-40' : 'translate-y-0',
    ]"
  >
    <!-- Wrapper utama yang mengatur semua item di dalamnya -->
    <div
      :class="[
        'py-4 flex justify-between items-center px-6',
        'border-b-[1.6px] border-neu-100', // Border ada di kedua state
        isSticky ? 'sm:px-2 lg:px-10 gap-8 sm:gap-4' : 'sm:px-4 lg:px-10',
      ]"
    >
      <!-- Burger Icon (Mobile) -->
      <div class="sm:hidden">
        <button @click="toggleSidebar" aria-label="Toggle sidebar">
          <HamburgerMenu class="size-5" />
        </button>
      </div>

      <!-- Logo -->
      <RouterLink
        :to="{ name: 'Home' }"
        :class="[
          'font-se font-semibold',
          isSticky
            ? 'hidden sm:block text-xl sm:order-1 md:text-2xl lg:text-3xl'
            : 'text-2xl md:text-3xl leading-[38px]',
        ]"
      >
        Bali<span class="text-pr-500">nara</span>
      </RouterLink>

      <!-- Search Bar (HANYA muncul saat sticky) -->
      <form
        v-if="isSticky"
        class="flex sm:max-w-[560px] sm:order-2 w-full items-center justify-between rounded-full outline outline-neu-200 p-1"
      >
        <div class="wrapper gap-2 ps-1.5 flex items-center w-full">
          <Search class="min-w-5" />
          <input
            type="text"
            class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none bg-transparent"
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

      <!-- Nav Items (Desktop) -->
      <ul
        :class="[
          'hidden sm:flex items-center font-medium text-neu-700',
          isSticky
            ? 'sm:order-3 text-base sm:text-sm lg:text-base gap-4 lg:gap-8 xl:gap-[60px]'
            : 'sm:gap-8 lg:gap-[60px]',
        ]"
      >
        <!-- Discover -->
        <li class="flex flex-col items-center justify-center group">
          <RouterLink
            :to="{ name: 'Destinations' }"
            class="transition-all duration-400 ease-in-out group-hover:text-pr-500"
            :class="{ 'text-pr-500': $route.name === 'Destinations' }"
            >Discover</RouterLink
          >
          <span
            class="w-0 h-[1.6px] bg-pr-500 rounded-full relative top-2 transition-all duration-500 ease-in-out group-hover:w-6"
            :class="{ 'w-6': $route.name === 'Destinations' }"
          ></span>
        </li>

        <li
          @click="toggleReviewDropdown"
          class="cursor-pointer relative reviews-dropdown flex flex-col items-center justify-center group"
        >
          <span class="transition-all duration-400 ease-in-out group-hover:text-pr-500"
            >Review</span
          >
          <span
            class="w-0 h-[1.6px] bg-pr-500 rounded-full relative top-2 transition-all duration-500 ease-in-out group-hover:w-6"
          ></span>
          <!-- Dropdown review menu -->
          <div
            v-if="isReviewOpen"
            class="z-50 absolute top-full left-0 mt-3 bg-sur-50 rounded-2xl p-2 shadow-md"
          >
            <ul class="flex flex-col gap-2" aria-labelledby="dropdownHoverButton">
              <li>
                <RouterLink
                  :to="{ name: 'WriteReview' }"
                  class="block whitespace-nowrap rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                  >Write a review</RouterLink
                >
              </li>
              <li>
                <RouterLink
                  :to="{ name: 'SuggestSpot' }"
                  class="block whitespace-nowrap rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                  >Suggest a spot</RouterLink
                >
              </li>
            </ul>
          </div>
        </li>

        <!-- About -->
        <li class="flex flex-col items-center justify-center group">
          <RouterLink
            :to="{ name: 'About' }"
            class="transition-all duration-400 ease-in-out group-hover:text-pr-500"
            :class="{ 'text-pr-500': $route.name === 'About' }"
            >About</RouterLink
          >
          <span
            class="w-0 h-[1.6px] bg-pr-500 rounded-full relative top-2 transition-all duration-500 ease-in-out group-hover:w-6"
            :class="{ 'w-6': $route.name === 'About' }"
          ></span>
        </li>
      </ul>

      <!-- User/Auth Section -->
      <div :class="{ 'sm:order-4': isSticky }">
        <div v-if="authStore.isAuthenticated">
          <div
            @click="toggleUserDropdown"
            class="rounded-full user-dropdown relative size-9 lg:size-11 border border-neu-200 cursor-pointer"
          >
            <img
              v-if="authStore.currentUser?.image"
              :src="authStore.currentUser.image"
              alt="User Profile"
              class="size-full object-cover rounded-full"
              @error="handleImageError"
            />
            <img
              v-else
              :src="defaultAvatar"
              alt="Default Profile"
              class="size-full rounded-full border border-neu-200 object-cover"
            />
            <!-- User Dropdown -->
            <div
              v-if="isUserOpen"
              class="z-50 absolute flex w-fit top-full right-0 mt-3 bg-sur-50 rounded-2xl p-2 shadow-md"
            >
              <ul class="flex flex-col gap-2">
                <li>
                  <RouterLink
                    :to="{ name: 'Profile' }"
                    class="flex w-full min-w-38 whitespace-nowrap text-start rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                    >Profile</RouterLink
                  >
                </li>
                <li>
                  <RouterLink
                    :to="{ name: 'Wishlist' }"
                    class="flex w-full min-w-38 whitespace-nowrap text-start rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                    >Wishlist</RouterLink
                  >
                </li>
                <li>
                  <RouterLink
                    :to="{ name: 'UserReview' }"
                    class="flex w-full min-w-38 whitespace-nowrap text-start rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                    >Reviews</RouterLink
                  >
                </li>
                <li>
                  <RouterLink
                    :to="{ name: 'UserSuggestion' }"
                    class="flex w-full min-w-38 whitespace-nowrap text-start rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                    >Suggests</RouterLink
                  >
                </li>
                <li>
                  <button
                    type="button"
                    @click="authStore.logout()"
                    class="flex w-full min-w-38 whitespace-nowrap text-start rounded-xl ps-3 pe-4.5 py-2 hover:bg-[#EFF6F2]"
                  >
                    Sign Out
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div
          v-else
          class="hidden cursor-pointer sm:flex px-4.5 py-2.5 gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white whitespace-nowrap"
          @click="isLoginOpen = true"
        >
          <Login :class="{ 'lg:flex': !isSticky, hidden: isSticky }" />
          Sign in
        </div>
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
