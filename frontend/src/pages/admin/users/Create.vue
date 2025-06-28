<script setup lang="ts">
import { ref } from 'vue' // Import ref
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Show from '@/components/icons/Show.vue'
import { RouterLink, useRouter } from 'vue-router' // Import useRouter untuk pengalihan
import axios from 'axios' // Asumsikan Anda menggunakan Axios untuk permintaan HTTP

const router = useRouter() // Inisialisasi router

const username = ref('')
const email = ref('')
const phoneNumber = ref('')
const password = ref('')
const showPassword = ref(false) // Untuk mengaktifkan/menonaktifkan visibilitas kata sandi

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

const createUser = async () => {
  try {
    const response = await axios.post('http://localhost:8000/api/users/create-admin/', {
      // Ganti dengan URL API Django Anda yang sebenarnya
      username: username.value,
      email: email.value,
      phone_number: phoneNumber.value, // Pastikan ini cocok dengan nama bidang Django Anda
      password: password.value,
    })
    console.log('User created successfully:', response.data)
    alert('Admin user created successfully!')
    router.push({ name: 'AdminUsers' }) // Arahkan kembali ke halaman manajemen pengguna
  } catch (error) {
    console.error('Error creating user:', error)
    if (axios.isAxiosError(error) && error.response) {
      // Tangani kesalahan validasi atau kesalahan lain dari backend
      console.error('Response data:', error.response.data)
      alert('Failed to create admin user: ' + JSON.stringify(error.response.data))
    } else {
      alert('An unexpected error occurred.')
    }
  }
}
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Create Admin</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Users</span>
        <ArrowRight class="size-4 text-neu-500" />
        <RouterLink :to="{ name: 'AdminUsers' }" class="hover:underline">Management</RouterLink>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Create</span>
      </div>
    </div>

    <div class="bg-sur-50 border border-neu-100 p-4 rounded-3xl flex flex-col gap-4 md:gap-8">
      <div class="flex flex-col md:flex-row gap-4 flex-1">
        <div class="flex flex-col flex-1 gap-3">
          <label for="username" class="text-base font-semibold">Username</label>
          <input
            type="text"
            id="username"
            v-model="username"
            placeholder="Username"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-1 flex-col gap-3">
          <label for="email" class="text-base font-semibold">Email</label>
          <input
            type="email"
            id="email"
            v-model="email"
            placeholder="Email"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
      </div>
      <div class="flex flex-col md:flex-row gap-4 flex-1">
        <div class="flex flex-1 flex-col gap-3">
          <label for="phoneNumber" class="text-base font-semibold">Phone Number</label>
          <input
            type="text"
            id="phoneNumber"
            v-model="phoneNumber"
            placeholder="Phone Number"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col flex-1 gap-3">
          <label for="password" class="text-base font-semibold">Password</label>
          <div class="relative flex">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="password"
              class="w-full border text-sm ps-3 pe-10 py-3 border-neu-200 rounded-full"
              placeholder="Password"
            />
            <Show
              class="size-5.5 absolute top-1/2 -translate-y-1/2 right-3 cursor-pointer"
              @click="togglePasswordVisibility"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="flex gap-2.5 items-center">
      <button
        type="submit"
        @click="createUser"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-pr-600 justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
      >
        Create
      </button>
      <RouterLink
        :to="{ name: 'AdminUsers' }"
        class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
      >
        Cancel
      </RouterLink>
    </div>
  </div>
</template>
