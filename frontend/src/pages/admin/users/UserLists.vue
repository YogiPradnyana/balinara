<script setup>
// --- IMPORTS ---
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

// --- Impor Ikon ---
import ArrowRight from '@/components/icons/ArrowRight.vue';
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue';
import Edit from '@/components/icons/Edit.vue';
import Plus from '@/components/icons/Plus.vue';
import Search from '@/components/icons/Search.vue';
import Show from '@/components/icons/Show.vue';
import TrashCan from '@/components/icons/TrashCan.vue';

// --- STATE MANAGEMENT ---
const users = ref([]);
const isLoading = ref(true);
const error = ref(null);
const totalUsers = ref(0);
const nextPageUrl = ref(null);
const previousPageUrl = ref(null);
const currentPage = ref(1);
const pageSize = ref(10); // Sesuaikan jika PAGE_SIZE di Django berbeda

// --- COMPUTED PROPERTIES ---
const startEntry = computed(() => {
  if (totalUsers.value === 0) return 0;
  return (currentPage.value - 1) * pageSize.value + 1;
});

const endEntry = computed(() => {
  const end = currentPage.value * pageSize.value;
  return Math.min(end, totalUsers.value);
});


// ===================================================================
// PENTING: PASTIKAN URL INI SUDAH 100% BENAR SESUAI DENGAN urls.py DJANGO ANDA
// Berdasarkan diskusi terakhir kita, ini adalah URL yang benar untuk Anda.
// ===================================================================
const API_BASE_URL = 'http://localhost:8000/api/users/';


// --- LOGIKA API LANGSUNG DI DALAM KOMPONEN ---

/**
 * Mengambil daftar pengguna dari server.
 * @param {string} [url=API_BASE_URL] - URL untuk di-fetch, bisa untuk paginasi.
 */
const fetchUsers = async (url = API_BASE_URL) => {
  isLoading.value = true;
  error.value = null;
  try {
    const token = localStorage.getItem('userToken');
    if (!token) {
        throw new Error('Token otentikasi tidak ditemukan. Silakan login kembali.');
    }

    const response = await axios.get(url, {
      headers: { 
        'Authorization': `Token ${token}` 
      }
    });

    if (response.data && Array.isArray(response.data.results)) {
      users.value = response.data.results;
      totalUsers.value = response.data.count;
      nextPageUrl.value = response.data.next;
      previousPageUrl.value = response.data.previous;

      const urlParams = new URL(url).searchParams;
      currentPage.value = parseInt(urlParams.get('page')) || 1;
    } else {
      throw new Error('Format data dari server tidak sesuai.');
    }
  } catch (err) {
    if (err.response) {
      if (err.response.status === 403) {
        error.value = 'Izin Ditolak. Pastikan Anda adalah Admin.';
      } else if (err.response.status === 404) {
        error.value = 'Endpoint Tidak Ditemukan. Periksa URL API.';
      } else {
        error.value = `Gagal memuat data: Error ${err.response.status}.`;
      }
    } else {
      error.value = 'Kesalahan Jaringan atau Server tidak merespons.';
    }
    console.error('Error saat fetchUsers:', err);
  } finally {
    isLoading.value = false;
  }
}

/**
 * Menghapus pengguna berdasarkan ID.
 * @param {number | string} userId - ID dari pengguna yang akan dihapus.
 * @param {string} username - Nama pengguna untuk pesan konfirmasi.
 */
const deleteUser = async (userId, username) => {
  const isConfirmed = window.confirm(`Apakah Anda yakin ingin menghapus pengguna "${username}"?`);
  if (!isConfirmed) return;

  try {
    const token = localStorage.getItem('userToken');
    if (!token) {
        alert('Token tidak ditemukan. Silakan login kembali.');
        return;
    }

    // Mengirim permintaan DELETE langsung dari komponen
    await axios.delete(`${API_BASE_URL}${userId}/`, {
      headers: { 
        'Authorization': `Token ${token}` 
      }
    });

    alert(`Pengguna "${username}" berhasil dihapus.`);
    
    // Refresh data. Jika ini halaman terakhir dan jadi kosong, mungkin perlu logika tambahan,
    // tapi untuk sekarang kita refresh halaman saat ini atau halaman pertama.
    fetchUsers(); 

  } catch (err) {
    alert('Gagal menghapus pengguna.');
    console.error('Error saat deleteUser:', err);
  }
};


// --- LIFECYCLE HOOK ---
onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Management</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Users</span> <ArrowRight class="size-4 text-neu-500" /> <span class="text-neu-500">Management</span>
      </div>
    </div>
    <div class="flex flex-col rounded-3xl border border-neu-100">
      <div class="flex flex-col p-4">
        <div class="flex justify-between sm:items-center flex-col sm:flex-row gap-4">
          <div class="border border-neu-100 gap-2 px-2.5 order-2 sm:order-1 py-2 flex items-center w-full sm:w-1/2 rounded-full">
            <Search class="size-6" />
            <input type="text" class="w-full text-xs md:text-sm focus:outline-none" placeholder="Search..." />
          </div>
          <RouterLink :to="{ name: 'AdminUserCreate' }" class="whitespace-nowrap flex px-4.5 order-1 sm:order-2 py-2.5 cursor-pointer w-fit hover:bg-pr-600 text-sm gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white">
            <Plus class="size-5" /> New User
          </RouterLink>
        </div>

        <div class="mt-4 overflow-hidden border border-neu-100 rounded-2xl">
          <div class="max-w-full overflow-x-auto">
            <table class="min-w-180 w-full">
              <thead class="bg-pr-500 text-xs text-white">
                <tr>
                  <th class="p-4 text-start font-semibold w-12">NO</th>
                  <th class="p-4 text-start font-semibold">USERNAME</th>
                  <th class="p-4 text-start font-semibold">EMAIL</th>
                  <th class="p-4 text-start font-semibold">PHONE</th>
                  <th class="p-4 text-start font-semibold">ROLE</th>
                  <th class="p-4 text-start font-semibold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                <tr v-if="isLoading"><td colspan="6" class="p-4 text-center text-neu-700">Memuat data...</td></tr>
                <tr v-else-if="error"><td colspan="6" class="p-4 text-center text-red-500">{{ error }}</td></tr>
                <tr v-else-if="users.length === 0"><td colspan="6" class="p-4 text-center text-neu-700">Tidak ada data pengguna.</td></tr>
                
                <template v-else>
                  <tr v-for="(user, index) in users" :key="user.id" class="text-sm text-neu-700 border-b border-neu-100">
                    <td class="p-4 text-neu-900">{{ startEntry + index }}</td>
                    <td class="p-4 text-neu-900 font-semibold">{{ user.username }}</td>
                    <td class="p-4">{{ user.email }}</td>
                    <td class="p-4">{{ user.phone || '-' }}</td>
                    <td class="p-4">{{ user.role ? (user.role.charAt(0).toUpperCase() + user.role.slice(1)) : '-' }}</td>
                    <td class="p-4 flex gap-3">
                      <button title="Edit" class="flex items-center justify-center p-2 rounded-md bg-[#FACA15] hover:bg-yellow-500"><Edit class="size-5 text-neu-900" /></button>
                      <button title="Detail" class="flex items-center justify-center p-2 rounded-md bg-[#295F98] hover:bg-blue-800"><Show class="size-5 text-white" /></button>
                      
                      <button @click="deleteUser(user.id, user.username)" title="Delete" class="flex items-center justify-center p-2 rounded-md bg-[#E02424] hover:bg-red-700">
                        <TrashCan class="size-5 text-white" />
                      </button>
                    </td>
                  </tr>
                </template>
              </tbody>
            </table>
          </div>
        </div>
        
        <div class="flex justify-between items-center gap-3 flex-wrap mt-3" v-if="!isLoading && users.length > 0">
          <div class="text-sm text-neu-600">
            Showing <span class="font-medium">{{ startEntry }}</span> to <span class="font-medium">{{ endEntry }}</span> of <span class="font-medium">{{ totalUsers }}</span> Entries
          </div>
          <div class="flex items-center rounded-lg overflow-hidden">
            <button @click="fetchUsers(previousPageUrl)" :disabled="!previousPageUrl" class="flex items-center gap-2 h-8 px-3 font-semibold bg-neu-100 hover:bg-neu-200 disabled:text-neu-400 disabled:cursor-not-allowed">
              <ArrowRight2Bold class="size-4 scale-x-[-1]" />Prev
            </button>
            <button @click="fetchUsers(nextPageUrl)" :disabled="!nextPageUrl" class="flex items-center gap-2 h-8 px-3 font-semibold bg-neu-100 hover:bg-neu-200 disabled:text-neu-400 disabled:cursor-not-allowed border-l border-neu-200">
              Next<ArrowRight2Bold class="size-4" />
            </button>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<style scoped>
button:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}
</style>