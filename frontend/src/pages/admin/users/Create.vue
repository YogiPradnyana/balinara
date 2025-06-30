<script setup lang="ts">
import { ref, onMounted } from 'vue' // Pastikan onMounted diimpor
import ArrowRight from '@/components/icons/ArrowRight.vue'
import Show from '@/components/icons/Show.vue'
import { RouterLink, useRouter } from 'vue-router'
import axios from 'axios'
import { toast } from 'vue-sonner'

const router = useRouter() 

// --- Inisialisasi Awal Form ---
// Ini adalah nilai default saat komponen pertama kali dibuat.
const adminForm = ref({
  username: '',
  email: '',
  phone: '', 
  password: '',
});
// ------------------------------

const showPassword = ref(false) 

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value
}

// --- PENTING: Reset form saat komponen dimuat (mounted) ---
onMounted(() => {
  // Pastikan form selalu kosong saat komponen pertama kali ditampilkan
  // Ini akan mengatasi masalah data lama yang persisten atau autofill yang salah saat form dimuat.
  adminForm.value = {
    username: '',
    email: '',
    phone: '',
    password: '',
  };
  console.log('Form direset saat mounted.');
});
// --------------------------------------------------------


const createUser = async () => {
  try {
    console.log('Data yang akan dikirim:', adminForm.value);

    const token = localStorage.getItem('userToken'); 
    if (!token) {
        toast.error('Anda belum login. Silakan login kembali.');
        router.push({ name: 'Login' });
        return;
    }

    const response = await axios.post('http://localhost:8000/api/users/create-admin/', {
      username: adminForm.value.username,
      email: adminForm.value.email,
      phone: adminForm.value.phone, 
      password: adminForm.value.password,
    }, {
      headers: {
        'Authorization': `Token ${token}`
      }
    });

    console.log('User created successfully:', response.data);
    toast.success('Admin user created successfully!'); 
    
    // Reset form setelah sukses submit
    adminForm.value = { 
      username: '', 
      email: '', 
      phone: '', 
      password: '' 
    };
    console.log('Form direset setelah sukses submit.');

    router.push({ name: 'AdminUsers' });
  } catch (error: any) {
    console.error('Error saat membuat user:', error);
    if (axios.isAxiosError(error) && error.response) {
      console.error('Response data:', error.response.data);
      let errorMessage = 'Gagal membuat admin: ';
      if (typeof error.response.data === 'object') {
        for (const key in error.response.data) {
          errorMessage += `${key}: ${JSON.stringify(error.response.data[key])}; `;
        }
      } else {
        errorMessage += error.response.data;
      }
      toast.error(errorMessage);
    } else {
      toast.error('Terjadi kesalahan tak terduga.');
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
            v-model="adminForm.username" 
            placeholder="Username"
            autocomplete="off" 
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-1 flex-col gap-3">
          <label for="email" class="text-base font-semibold">Email</label>
          <input
            type="email"
            id="email"
            v-model="adminForm.email" 
            placeholder="Email"
            autocomplete="off" 
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
      </div>
      <div class="flex flex-col md:flex-row gap-4 flex-1">
        <div class="flex flex-1 flex-col gap-3">
          <label for="phone" class="text-base font-semibold">Phone Number</label> 
          <input
            type="text"
            id="phone" 
            v-model="adminForm.phone" 
            placeholder="Phone Number"
            autocomplete="off"
            class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
          />
        </div>
        <div class="flex flex-col flex-1 gap-3">
          <label for="password" class="text-base font-semibold">Password</label>
          <div class="relative flex">
            <input
              :type="showPassword ? 'text' : 'password'"
              id="password"
              v-model="adminForm.password" 
              class="w-full border text-sm ps-3 pe-10 py-3 border-neu-200 rounded-full"
              placeholder="Password"
              autocomplete="new-password"
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
        @click.prevent="createUser" 
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