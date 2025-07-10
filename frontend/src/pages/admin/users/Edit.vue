<script setup>
// --- IMPORTS ---
import { ref, onMounted } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import ArrowRight from '@/components/icons/ArrowRight.vue';
import axios from 'axios';

// --- STATE MANAGEMENT ---
const route = useRoute();
const router = useRouter();

// Definisikan reactive state untuk data pengguna (profil)
const user = ref({
  username: '',
  email: '',
  phone: '', // Pastikan ini 'phone' sesuai serializer Django Anda
  is_active: true,
  is_staff: false,
});

// Definisikan reactive state untuk data password baru
const passwordForm = ref({
  new_password: '',
  new_password2: '',
});

const isLoading = ref(true); // Untuk loading profil user
const error = ref(null); // Untuk error profil user

const isPasswordChanging = ref(false); // Untuk loading perubahan password
const passwordError = ref(null); // Untuk error perubahan password

const userId = ref(route.params.id);

// BASE URL API untuk operasi user management
// Ini harus sama dengan API_BASE_URL di UserLists.vue
const API_BASE_URL = 'http://localhost:8000/api/users/';

// --- LOGIKA API PROFIL PENGGUNA ---
const fetchUser = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const token = localStorage.getItem('userToken');
    if (!token) {
        throw new Error('Token otentikasi tidak ditemukan. Silakan login kembali.');
    }
    
    const response = await axios.get(`${API_BASE_URL}${userId.value}/`, {
      headers: { 'Authorization': `Token ${token}` }
    });
    const { username, email, phone, is_active, is_staff } = response.data;
    user.value = { username, email, phone, is_active, is_staff };
    
  } catch (err) {
    console.error('Error fetching user profile:', err);
    if (axios.isAxiosError(err) && err.response) {
        if (err.response.status === 403) {
            error.value = 'Izin Ditolak. Pastikan Anda adalah Admin dan memiliki akses ke pengguna ini.';
        } else if (err.response.status === 404) {
            error.value = 'Pengguna tidak ditemukan. Pastikan ID pengguna valid.';
        } else if (err.response.status === 401) {
            error.value = 'Tidak Terautentikasi. Silakan login kembali.';
        } else {
            error.value = `Gagal memuat data: Error ${err.response.status}. Detail: ${err.response.data?.detail || JSON.stringify(err.response.data)}.`;
        }
    } else {
        error.value = `Terjadi kesalahan saat memuat profil: ${err.message}.`;
    }
  } finally {
    isLoading.value = false;
  }
};

const saveUser = async () => {
  error.value = null;
  try {
    const token = localStorage.getItem('userToken');
    if (!token) {
        throw new Error('Token otentikasi tidak ditemukan. Silakan login kembali.');
    }
    await axios.put(`${API_BASE_URL}${userId.value}/`, user.value, {
      headers: { 'Authorization': `Token ${token}` }
    });
    alert('Profil pengguna berhasil diperbarui!');
    router.push({ name: 'AdminUsers' });
  } catch (err) {
    console.error('Error saving user profile:', err);
    if (axios.isAxiosError(err) && err.response) {
        error.value = `Gagal menyimpan profil: Error ${err.response.status}. Detail: ${err.response.data?.detail || JSON.stringify(err.response.data)}.`;
        if (err.response.data && typeof err.response.data === 'object') {
            for (const key in err.response.data) {
                if (Object.prototype.hasOwnProperty.call(err.response.data, key)) {
                    error.value += `\n${key}: ${err.response.data[key]}`;
                }
            }
        }
    } else {
        error.value = `Terjadi kesalahan saat menyimpan profil: ${err.message}.`;
    }
  }
};

// --- LOGIKA API EDIT PASSWORD ADMIN ---
const changePassword = async () => {
  isPasswordChanging.value = true;
  passwordError.value = null;

  // Validasi frontend dasar
  if (passwordForm.value.new_password !== passwordForm.value.new_password2) {
    passwordError.value = "Konfirmasi kata sandi baru tidak cocok.";
    isPasswordChanging.value = false;
    return;
  }
  if (!passwordForm.value.new_password) {
    passwordError.value = "Kata sandi baru tidak boleh kosong.";
    isPasswordChanging.value = false;
    return;
  }

  try {
    const token = localStorage.getItem('userToken');
    if (!token) {
        throw new Error('Token otentikasi tidak ditemukan. Silakan login kembali.');
    }

    // Endpoint untuk admin set password
    // URL: http://localhost:8000/api/users/{id}/set-password/
    await axios.post(`${API_BASE_URL}${userId.value}/set-password/`, passwordForm.value, {
      headers: { 'Authorization': `Token ${token}` }
    });

    alert('Kata sandi pengguna berhasil diperbarui!');
    passwordForm.value.new_password = ''; // Bersihkan form
    passwordForm.value.new_password2 = '';
  } catch (err) {
    console.error('Error changing password:', err);
    if (axios.isAxiosError(err) && err.response) {
        passwordError.value = `Gagal mengubah kata sandi: ${err.response.status}. Detail: ${err.response.data?.new_password || err.response.data?.new_password2 || err.response.data?.detail || JSON.stringify(err.response.data)}.`;
    } else {
        passwordError.value = `Terjadi kesalahan saat mengubah kata sandi: ${err.message}.`;
    }
  } finally {
    isPasswordChanging.value = false;
  }
};


// --- LIFECYCLE HOOK ---
onMounted(() => {
  if (userId.value) {
    fetchUser();
  } else {
    error.value = 'ID pengguna tidak ditemukan di URL. Tidak dapat memuat data profil.';
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="space-y-6">
    <div class="flex flex-col">
      <h1 class="text-3xl font-se font-semibold">Edit Admin</h1>
      <div class="flex gap-2 items-center font-medium">
        <span>Users</span>
        <ArrowRight class="size-4 text-neu-500" />
        <RouterLink :to="{ name: 'AdminUsers' }" class="hover:underline">Management</RouterLink>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Edit</span>
      </div>
    </div>

    <div v-if="isLoading" class="text-center text-lg text-gray-600">Memuat data pengguna...</div>
    <div v-else-if="error" class="text-center text-red-600 text-lg p-4 border border-red-300 rounded-lg bg-red-50">{{ error }}</div>

    <div v-else class="bg-sur-50 border border-neu-100 p-4 rounded-3xl flex flex-col gap-4 md:gap-8">
      <h2 class="text-xl font-semibold">Informasi Profil</h2>
      <form @submit.prevent="saveUser">
        <div class="flex flex-col md:flex-row gap-4 flex-1">
          <div class="flex flex-col flex-1 gap-3">
            <label for="username" class="text-base font-semibold">Username</label>
            <input
              type="text"
              id="username"
              placeholder="Username"
              v-model="user.username"
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
          </div>
          <div class="flex flex-1 flex-col gap-3">
            <label for="email" class="text-base font-semibold">Email</label>
            <input
              type="email"
              id="email"
              placeholder="Email"
              v-model="user.email"
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
          </div>
        </div>

        <div class="flex flex-col md:flex-row gap-4 flex-1 mt-4">
          <div class="flex flex-1 flex-col gap-3">
            <label for="phone" class="text-base font-semibold">Phone Number</label>
            <input
              type="text"
              id="phone"
              placeholder="Phone Number"
              v-model="user.phone"
              class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
            />
          </div>
          <div class="flex flex-1 flex-col gap-3 justify-end items-start pb-2">
            <div class="flex items-center">
              <input
                type="checkbox"
                id="is_active"
                v-model="user.is_active"
                class="h-5 w-5 text-pr-500 rounded border-neu-300 focus:ring-pr-500"
              />
              <label for="is_active" class="ml-2 text-base font-semibold">Active User</label>
            </div>
          </div>
        </div>

        <div class="flex flex-col md:flex-row gap-4 flex-1 mt-4">
            <div class="flex flex-1 flex-col gap-3 justify-end items-start pb-2">
                <div class="flex items-center">
                    <input
                        type="checkbox"
                        id="is_staff"
                        v-model="user.is_staff"
                        class="h-5 w-5 text-pr-500 rounded border-neu-300 focus:ring-pr-500"
                    />
                    <label for="is_staff" class="ml-2 text-base font-semibold">Admin/Staff User</label>
                </div>
            </div>
            <div class="flex flex-col flex-1 gap-3"></div>
        </div>

        <div class="flex gap-2.5 items-center mt-8">
          <button
            type="submit"
            class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-pr-600 justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
          >
            Save Profile
          </button>
          <RouterLink
            :to="{ name: 'AdminUsers' }"
            class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-[#F0F0F0] justify-center text-sm md:text-base font-medium leading-6 bg-sur-50 rounded-full border border-neu-900"
          >
            Cancel
          </RouterLink>
        </div>
      </form>
    </div>

    <div class="bg-sur-50 border border-neu-100 p-4 rounded-3xl flex flex-col gap-4 md:gap-8 mt-6">
        <h2 class="text-xl font-semibold">Ganti Kata Sandi</h2>
        <form @submit.prevent="changePassword">
            <div class="flex flex-col gap-3">
                <label for="new_password" class="text-base font-semibold">Kata Sandi Baru</label>
                <input
                    type="password"
                    id="new_password"
                    placeholder="Kata Sandi Baru"
                    v-model="passwordForm.new_password"
                    class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                    autocomplete="new-password"
                />
            </div>
            <div class="flex flex-col gap-3 mt-4">
                <label for="new_password2" class="text-base font-semibold">Konfirmasi Kata Sandi Baru</label>
                <input
                    type="password"
                    id="new_password2"
                    placeholder="Konfirmasi Kata Sandi Baru"
                    v-model="passwordForm.new_password2"
                    class="px-3 py-3 text-sm border placeholder:text-neu-500 border-neu-200 rounded-full"
                    autocomplete="new-password"
                />
            </div>

            <div v-if="passwordError" class="text-red-600 text-sm mt-3">{{ passwordError }}</div>

            <div class="flex gap-2.5 items-center mt-8">
                <button
                    type="submit"
                    :disabled="isPasswordChanging"
                    class="px-6 py-2 flex gap-2 items-center cursor-pointer hover:bg-pr-600 justify-center text-sm md:text-base font-medium leading-6 bg-pr-500 rounded-full text-neu-50"
                >
                    <span v-if="isPasswordChanging">Mengubah...</span>
                    <span v-else>Ubah Kata Sandi</span>
                </button>
            </div>
        </form>
    </div>
  </div>
</template>