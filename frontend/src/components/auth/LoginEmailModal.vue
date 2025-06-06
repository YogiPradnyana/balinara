<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import ArrowLeftBold from '../icons/ArrowLeftBold.vue'
import Exit from '../icons/Exit.vue'
import Show from '../icons/Show.vue'
import Hide from '../icons/Hide.vue'

const emit = defineEmits(['closeLoginEmail', 'closeAll', 'switchRegister'])

const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const showPassword = ref(false)

const localError = ref(null)

const handleClose = (close) => {
  localError.value = null
  close ? emit('closeAll') : emit('closeLoginEmail')
}
const handleSwitch = () => {
  localError.value = null
  emit('switchRegister')
}

const handleSubmitLogin = async () => {
  localError.value = null // Reset error lokal sebelum mencoba login
  // Panggil action login dari authStore
  try {
    await authStore.login({
      email: email.value,
      password: password.value,
    })
    // Jika login berhasil, action di store akan menangani navigasi.
    // Komponen parent yang menampilkan modal ini bisa mendengarkan
    // perubahan state `isAuthenticated` di store untuk menutup modal secara otomatis.
    // Atau, emit event sukses jika diperlukan.
    emit('closeLoginEmail') // Tutup modal login ini setelah berhasil
  } catch (error) {
    // Tangkap error yang di-throw oleh action login di store
    // authStore.authError akan berisi pesan error dari store
    // Kita bisa tampilkan itu atau pesan kustom
    localError.value = authStore.authError || 'An unexpected error occurred.'
    console.error('Login failed in modal:', error)
  }
}

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}
</script>
<template>
  <!-- Overlay -->
  <div
    class="fixed inset-0 font-pr p-4 text-neu-900 bg-neu-900/50 flex items-center justify-center z-999"
  >
    <div
      class="bg-white px-4 pt-4 pb-8 flex-col flex items-end rounded-3xl w-full max-w-sm md:max-w-md animate-fadeIn"
    >
      <div class="flex justify-between items-center w-full">
        <ArrowLeftBold
          class="size-5 cursor-pointer hover:text-neu-500 transition"
          @click="handleClose(false)"
          aria-label="Back"
        />
        <Exit
          class="size-5 cursor-pointer hover:text-neu-500 transition"
          @click="handleClose(true)"
          aria-label="Close"
        />
      </div>
      <div class="w-full flex flex-col items-center mt-4 px-4">
        <h1
          class="text-[28px] md:text-[32px] text-center font-semibold leading-7 font-se md:leading-[38px]"
        >
          Bali<span class="text-pr-500">nara</span>
        </h1>
        <div
          class="flex gap-2 sm:gap-2.5 mt-5 md:mt-6 p-1 items-center w-fit rounded-full bg-sur-100"
        >
          <button
            type="button"
            class="px-8 sm:px-10 md:px-12 py-2 flex gap-2 items-center justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
            aria-pressed="true"
          >
            Sign in
          </button>
          <button
            type="button"
            @click="handleSwitch"
            class="cursor-pointer px-8 sm:px-10 md:px-12 py-2 flex gap-2 items-center justify-center text-sm md:text-base font-medium leading-6 bg-none rounded-full text-neu-500"
            aria-pressed="false"
          >
            Sign up
          </button>
        </div>
        <h2 class="text-lg sm:text-xl font-semibold mt-4 md:mt-6 leading-8 w-full">
          Welcome back.
        </h2>
        <form class="flex flex-col w-full" @submit.prevent="handleSubmitLogin">
          <div class="space-y-4 mt-5 md:mt-8 w-full">
            <div class="flex flex-col gap-3">
              <label class="text-sm font-semibold">Email</label>
              <input
                v-model="email"
                id="login-email"
                type="email"
                class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                placeholder="Enter your email"
                required
                aria-required="true"
              />
            </div>
            <div class="flex flex-col gap-3">
              <label class="text-sm font-semibold">Password</label>
              <div class="relative flex">
                <input
                  v-model="password"
                  id="login-password"
                  :type="showPassword ? 'text' : 'password'"
                  class="w-full border text-sm ps-3 pe-10 py-3 border-neu-200 rounded-full"
                  placeholder="Enter your password"
                  required
                  aria-required="true"
                />
                <button
                  type="button"
                  @click="togglePasswordVisibility"
                  class="absolute top-1/2 -translate-y-1/2 right-3 text-neu-500 hover:text-neu-700 p-1"
                  :aria-label="showPassword ? 'Hide password' : 'Show password'"
                  aria-pressed="showPassword"
                >
                  <component :is="showPassword ? Hide : Show" class="size-5" />
                </button>
              </div>
            </div>
            <p class="text-sm font-medium underline hover:text-pr-500 cursor-pointer transition">
              Forgot password?
            </p>
          </div>
          <div v-if="localError || authStore.isLoading" class="mt-4 text-center">
            <p v-if="authStore.isLoading" class="text-sm text-pr-500">Signing in...</p>
            <p v-if="localError && !authStore.isLoading" class="text-sm text-red-600">
              {{ localError }}
            </p>
          </div>
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="px-4.5 w-full py-2.5 md:py-3 flex gap-2 mt-8 items-center justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50 hover:bg-pr-600 focus:outline-none focus:ring-2 focus:ring-pr-500 focus:ring-offset-2 disabled:opacity-70 disabled:cursor-not-allowed transition"
          >
            {{ authStore.isLoading ? 'Processing...' : 'Sign in' }}
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.animate-fadeIn {
  animation: fadeIn 0.3s ease-out forwards;
}
</style>
