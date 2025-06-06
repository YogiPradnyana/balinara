<script setup>
import { ref } from 'vue'
import { useAuthStore } from '@/stores/authStore'
import ArrowLeftBold from '../icons/ArrowLeftBold.vue'
import Exit from '../icons/Exit.vue'
import Show from '../icons/Show.vue'
import Hide from '../icons/Hide.vue'

const emit = defineEmits(['closeRegisterEmail', 'closeAll', 'switchLogin'])

const authStore = useAuthStore()

const username = ref('')
const email = ref('')
const password = ref('')
const showPassword = ref(false)

const localError = ref(null)
// Untuk menyimpan error per field dari backend jika ada
const fieldErrors = ref({})

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const handleClose = (close) => {
  localError.value = null
  fieldErrors.value = {}
  authStore.error = null
  close ? emit('closeAll') : emit('closeRegisterEmail')
}
const handleSwitch = () => {
  localError.value = null
  fieldErrors.value = {}
  authStore.error = null
  emit('switchLogin')
}

const handleSubmitRegister = async () => {
  localError.value = null
  fieldErrors.value = {}
  authStore.error = null

  if (!username.value.trim() || !email.value.trim() || !password.value.trim()) {
    localError.value = 'All fields are required.'
    // Anda bisa set fieldErrors juga jika mau per field
    if (!username.value.trim()) fieldErrors.value.username = ['Username is required.']
    if (!email.value.trim()) fieldErrors.value.email = ['Email is required.']
    if (!password.value.trim()) fieldErrors.value.password = ['Password is required.']
    return
  }
  const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailPattern.test(email.value)) {
    localError.value = 'Please enter a valid email address.'
    fieldErrors.value.email = ['Please enter a valid email address.']
    return
  }
  // Anda bisa menambahkan validasi panjang password minimal di frontend juga
  if (password.value.length < 8) {
    // Contoh panjang minimal 8
    localError.value = 'Password must be at least 8 characters long.'
    fieldErrors.value.password = ['Password must be at least 8 characters long.']
    return
  }

  const payload = {
    username: username.value,
    email: email.value,
    password: password.value,
  }

  try {
    await authStore.register(payload)
    emit('closeRegisterEmail')
  } catch (error) {
    if (
      typeof error === 'object' &&
      error !== null &&
      !Array.isArray(error) &&
      Object.keys(error).length > 0 &&
      !(error instanceof Error)
    ) {
      fieldErrors.value = error
      const firstKey = Object.keys(error)[0]
      // Gabungkan semua pesan error untuk field pertama (jika ada > 1)
      localError.value = error[firstKey]
        ? `${firstKey}: ${error[firstKey].join(', ')}`
        : 'Registration failed. Please check the form.'
    } else {
      localError.value = error.message || authStore.authError || 'An unexpected error occurred.'
    }
    console.error('Registration failed in modal:', error)
  }
}
</script>
<template>
  <!-- Overlay -->
  <div
    class="fixed inset-0 font-pr p-4 text-neu-900 bg-neu-900/50 flex items-center justify-center z-999"
  >
    <div
      class="bg-white px-4 pt-4 pb-8 flex-col flex items-end rounded-3xl w-full max-w-sm md:max-w-lg animate-fadeIn"
    >
      <div class="flex justify-between items-center w-full">
        <ArrowLeftBold
          class="size-5 cursor-pointer hover:text-neu-500 transition"
          @click="handleClose(false)"
        />
        <Exit
          class="size-5 cursor-pointer hover:text-neu-500 transition"
          @click="handleClose(true)"
        />
      </div>
      <div class="w-full flex flex-col items-center mt-4 px-4">
        <h1
          class="text-[28px] md:text-[32px] text-center font-se font-semibold leading-7 md:leading-[38px]"
        >
          Bali<span class="text-pr-500">nara</span>
        </h1>
        <div
          class="flex gap-2 sm:gap-2.5 mt-5 md:mt-6 p-1 items-center w-fit rounded-full bg-sur-100"
        >
          <button
            type="button"
            @click="handleSwitch"
            class="px-8 sm:px-10 md:px-12 cursor-pointer py-2 flex gap-2 items-center justify-center text-sm md:text-base font-medium leading-6 bg-none rounded-full text-neu-500"
            aria-pressed="false"
          >
            Sign in
          </button>
          <button
            type="button"
            class="px-8 sm:px-10 md:px-12 py-2 flex gap-2 items-center justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
            aria-pressed="true"
          >
            Sign up
          </button>
        </div>
        <div class="flex w-full">
          <h2 class="text-lg sm:text-xl font-semibold mt-4 md:mt-6 leading-8 w-full md:max-w-72">
            Join Balinara to start your Bali journey.
          </h2>
        </div>
        <form class="flex flex-col w-full" @submit.prevent="handleSubmitRegister">
          <div class="space-y-4 mt-5 md:mt-8 w-full">
            <div class="flex flex-col gap-3">
              <label for="reg-username" class="text-sm font-semibold">Username</label>
              <input
                v-model="username"
                id="reg-username"
                type="text"
                class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                :class="{ 'border-red-500': fieldErrors.username }"
                placeholder="Choose a username"
                required
                aria-required="true"
              />
              <p v-if="fieldErrors.username" class="text-xs text-red-500 -mt-2">
                {{ fieldErrors.username[0] }}
              </p>
            </div>
            <div class="flex flex-col gap-3">
              <label for="reg-email" class="text-sm font-semibold">Email Address</label>
              <input
                v-model="email"
                id="reg-email"
                type="email"
                class="w-full border text-sm px-3 py-3 border-neu-200 rounded-full"
                :class="{ 'border-red-500': fieldErrors.email }"
                placeholder="Enter your email"
                required
                aria-required="true"
              />
              <p v-if="fieldErrors.email" class="text-xs text-red-500 -mt-2">
                {{ fieldErrors.email[0] }}
              </p>
            </div>
            <div class="flex flex-col gap-3">
              <label for="reg-password" class="text-sm font-semibold">Create a Password</label>
              <div class="relative flex">
                <input
                  v-model="password"
                  id="reg-password"
                  :type="showPassword ? 'text' : 'password'"
                  class="w-full border text-sm ps-3 pe-10 py-3 border-neu-200 rounded-full"
                  :class="{ 'border-red-500': fieldErrors.password }"
                  placeholder="Enter a strong password"
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
              <p v-if="fieldErrors.password" class="text-xs text-red-500 -mt-2">
                {{ fieldErrors.password[0] }}
              </p>
            </div>
          </div>
          <!-- Tampilkan pesan error umum atau loading state -->
          <div v-if="localError || authStore.isLoading" class="mt-4 text-left w-full">
            <p v-if="authStore.isLoading" class="text-sm text-pr-500 text-center">
              Creating account...
            </p>
            <!-- Tampilkan localError jika bukan error validasi field -->
            <p
              v-if="localError && !Object.keys(fieldErrors).length && !authStore.isLoading"
              class="text-sm text-red-600"
            >
              {{ localError }}
            </p>
          </div>
          <button
            type="submit"
            :disabled="authStore.isLoading"
            class="px-4.5 w-full py-2.5 md:py-3 flex gap-2 mt-8 items-center justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
          >
            {{ authStore.isLoading ? 'Processing...' : 'Sign up' }}
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
