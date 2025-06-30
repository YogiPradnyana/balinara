<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
// Import useRouter dari vue-router jika Anda berencana mengarahkan pengguna
// setelah error otentikasi (misalnya, kembali ke halaman login)
// import { useRouter } from 'vue-router';

// Impor ikon-ikon yang digunakan di template Anda
import ArrowRight from '@/components/icons/ArrowRight.vue'
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue'
import Edit from '@/components/icons/Edit.vue'
import Plus from '@/components/icons/Plus.vue'
import Search from '@/components/icons/Search.vue'
import Show from '@/components/icons/Show.vue'
import TrashCan from '@/components/icons/TrashCan.vue'

// Definisikan state reaktif untuk menyimpan data, status loading, dan pesan error
const users = ref([]) // Array untuk menyimpan daftar pengguna
const isLoading = ref(true) // Indikator loading data, dimulai sebagai true
const error = ref(null) // Pesan error jika terjadi masalah, dimulai sebagai null

// Inisialisasi router jika Anda menggunakannya (uncomment baris di bawah ini dan di atas)
// const router = useRouter(); 

// Fungsi asinkron untuk mengambil data pengguna dari API Django
const fetchUsers = async () => {
  console.log('--- Memulai fetchUsers ---'); // Log awal proses
  try {
    isLoading.value = true; // Pastikan loading diatur ke true di awal setiap panggilan
    error.value = null; // Reset pesan error sebelumnya
    
    // Ambil token otentikasi dari localStorage.
    // Kunci 'userToken' digunakan karena ini yang terlihat di tangkapan layar localStorage Anda.
    const token = localStorage.getItem('userToken'); 
    console.log('Token dari localStorage:', token ? 'Ada' : 'Tidak Ada', token); // Log token itu sendiri untuk verifikasi

    // Periksa apakah token ada. Jika tidak ada, pengguna belum login atau token hilang/kadaluarsa.
    if (!token) {
      error.value = 'Anda belum login atau sesi telah berakhir. Silakan login kembali.';
      isLoading.value = false; // Hentikan loading karena tidak ada token
      console.log('FetchUsers dihentikan: Token tidak ditemukan.');
      // Opsional: Arahkan pengguna ke halaman login jika token tidak ditemukan
      // if (router) router.push({ name: 'Login' }); 
      return; // Hentikan eksekusi fungsi
    }

    console.log('Melakukan permintaan GET ke http://localhost:8000/api/users/ dengan Authorization header.');
    // Lakukan permintaan GET ke API Django untuk daftar pengguna.
    // URL API yang benar kini adalah 'http://localhost:8000/api/users/'
    // Pastikan header Authorization dikirim. Karena token Anda terlihat seperti DRF Token Authentication,
    // formatnya adalah 'Token <string_token>'
    const response = await axios.get('http://localhost:8000/api/users/', {
      headers: {
        'Authorization': `Token ${token}` // Menggunakan 'Token' prefix untuk otentikasi
      }
    });

    console.log('Respons API diterima:', response.data); // Log seluruh data respons dari API

    // Pastikan respons data adalah array sebelum memprosesnya
    if (Array.isArray(response.data)) {
        // Filter keluar entri yang bernilai null atau undefined dari array respons
        users.value = response.data.filter(user => user !== null && user !== undefined);
        console.log('users.value setelah filtering null:', users.value); // Log array setelah filtering
        if (users.value.length === 0) {
            console.log('API mengembalikan array kosong setelah filtering.'); // Pesan jika array kosong
        }
    } else {
        // Jika respons bukan array, set pesan error dan kosongkan data users
        error.value = 'Format data dari server tidak sesuai. Diharapkan array.';
        users.value = []; 
        console.error('API response is not an array:', response.data); // Log error format
    }

  } catch (err) {
    // Tangani error yang mungkin terjadi selama permintaan API
    console.error('Terjadi error dalam fetchUsers (catch block):', err); // Log error lengkap dari try-catch
    if (err.response) {
      // Jika ada respons dari server (misalnya, kode status HTTP error)
      console.error('Respons error dari server (err.response):', err.response); // Log seluruh objek respons error
      console.error('Data error dari server (err.response.data):', err.response.data); // Log data error spesifik dari server
      
      if (err.response.status === 401) {
        // Error 401 Unauthorized: Token tidak valid atau kadaluarsa.
        error.value = 'Tidak terautentikasi. Token tidak valid atau kadaluarsa. Silakan login kembali.';
        // Hapus token dan data user yang mungkin sudah tidak valid dari localStorage
        localStorage.removeItem('userToken'); 
        localStorage.removeItem('userData'); 
        console.log('Token dan userData dihapus dari localStorage karena 401.');
        // Opsional: Arahkan kembali pengguna ke halaman login
        // if (router) router.push({ name: 'Login' });
      } else if (err.response.status === 403) {
        // Error 403 Forbidden: Pengguna terautentikasi tetapi tidak memiliki izin (bukan admin).
        error.value = 'Anda tidak memiliki izin (bukan admin) untuk melihat data ini. Pastikan Anda masuk sebagai Admin.';
      } else {
        // Error lain dari server (misalnya 400 Bad Request, 500 Internal Server Error)
        error.value = `Gagal memuat data user: ${err.response.status} - ${err.response.statusText}.`;
      }
    } else {
      // Jika tidak ada respons dari server (misalnya masalah jaringan, server down)
      error.value = 'Terjadi kesalahan jaringan atau server tidak merespons.';
      console.error('Tidak ada respons server (kemungkinan masalah jaringan atau CORS blocking):', err);
    }
  } finally {
    isLoading.value = false; // Selalu set loading menjadi false setelah permintaan selesai (baik berhasil maupun gagal)
    console.log('--- fetchUsers selesai. Final State: isLoading:', isLoading.value, 'error:', error.value, 'users count:', users.value.length, '---'); // Log status akhir
  }
}

// Fungsi getUserRole ini telah dihilangkan karena Anda sekarang menampilkan user.role secara langsung dari API
// Jika Anda masih membutuhkannya karena alasan tertentu (misalnya, untuk logika yang lebih kompleks dari sekadar menampilkan string),
// Anda bisa mengembalikan dan menyesuaikannya.

// Lifecycle hook: Panggil fetchUsers saat komponen selesai di-mount ke DOM
onMounted(() => {
  fetchUsers();
})
</script>

<template>
  <div class="space-y-6">
    <!-- Bagian Header Halaman -->
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Management</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Users</span>
        <ArrowRight class="size-4 text-neu-500" />
        <span class="text-neu-500">Management</span>
      </div>
    </div>

    <!-- Bagian Konten Utama: Tabel Manajemen User -->
    <div class="flex flex-col rounded-3xl border border-neu-100">
      <div class="flex flex-col p-4">
        <!-- Area Search Bar dan Tombol 'New Admin' -->
        <div class="flex justify-between sm:items-center flex-col sm:flex-row gap-4">
          <div
            class="border border-neu-100 gap-2 px-2.5 order-2 sm:order-1 py-2 flex items-center w-full sm:w-1/2 rounded-full"
          >
            <Search class="size-6" />
            <input
              type="text"
              class="w-full text-xs md:text-sm leading-5 placeholder:text-neu-500 focus:outline-none"
              placeholder="Search something..."
            />
          </div>
          <!-- Link untuk navigasi ke halaman pembuatan admin baru. -->
          <!-- Pastikan nama rute 'AdminUserCreate' sudah terdaftar di Vue Router Anda. -->
          <RouterLink
            :to="{ name: 'AdminUserCreate' }"
            class="whitespace-nowrap flex px-4.5 order-1 sm:order-2 py-2.5 cursor-pointer w-fit hover:bg-pr-600 text-sm gap-2 items-center justify-center font-medium bg-pr-500 rounded-full text-white"
          >
            <Plus class="size-5" />
            New Admin
          </RouterLink>
        </div>

        <!-- Area Tabel untuk Menampilkan Data User -->
        <div class="mt-4 overflow-hidden border border-neu-100 rounded-2xl">
          <div class="max-w-full overflow-x-auto">
            <table class="min-w-180 w-full">
              <thead class="bg-pr-500 text-xs text-white">
                <tr>
                  <th class="p-4 text-start font-semibold w-12">NO</th>
                  <th class="p-4 text-start font-semibold">USERNAME</th>
                  <th class="p-4 text-start font-semibold">EMAIL</th>
                  <th class="p-4 text-start font-semibold">PHONE NUMBER</th>
                  <th class="p-4 text-start font-semibold">ROLE</th>
                  <th class="p-4 text-start font-semibold">ACTION</th>
                </tr>
              </thead>
              <tbody>
                <!-- Kondisi: Menampilkan pesan "Memuat data..." saat isLoading true -->
                <tr v-if="isLoading">
                  <td colspan="6" class="p-4 text-center text-neu-700">Memuat data...</td>
                </tr>
                <!-- Kondisi: Menampilkan pesan error jika ada error -->
                <tr v-else-if="error">
                  <td colspan="6" class="p-4 text-center text-red-500">{{ error }}</td>
                </tr>
                <!-- Kondisi: Menampilkan pesan jika tidak ada data user setelah loading selesai -->
                <tr v-else-if="users.length === 0">
                  <td colspan="6" class="p-4 text-center text-neu-700">Tidak ada data user.</td>
                </tr>
                <!-- Loop untuk menampilkan setiap baris data user -->
                <tr
                  v-for="(user, index) in users"
                  :key="user.id"
                  class="text-sm text-neu-700 border-b border-neu-100"
                >
                  <td class="p-4 text-neu-900">{{ index + 1 }}</td>
                  <td class="p-4 text-neu-900 font-semibold">{{ user.username }}</td>
                  <td class="p-4">{{ user.email }}</td>
                  <td class="p-4">{{ user.phone || '-' }}</td> <!-- Menampilkan nomor telepon atau '-' jika kosong -->
                  
                  <!-- Langsung menampilkan user.role dari API, dengan kapitalisasi huruf pertama -->
                  <td class="p-4">{{ user.role ? (user.role.charAt(0).toUpperCase() + user.role.slice(1)) : '-' }}</td>

                  <td class="p-4 flex gap-3">
                    <!-- Tombol Edit User: Navigasi ke halaman edit dengan ID user -->
                    <RouterLink
                      :to="{ name: 'AdminUserEdit', params: { id: user.id } }"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#F0BF05] bg-[#FACA15]"
                    >
                      <Edit class="size-5 text-neu-900" />
                    </RouterLink>
                    <!-- Tombol Lihat Detail User: Navigasi ke halaman detail dengan ID user -->
                    <RouterLink
                      :to="{ name: 'AdminUserDetail', params: { id: user.id } }"
                      type="button"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#214B78] bg-[#295F98]"
                    >
                      <Show class="size-5 text-neu-50" />
                    </RouterLink>
                    <!-- Tombol Hapus User (belum ada logika delete di sini, hanya UI) -->
                    <button
                      type="button"
                      class="flex items-center justify-center p-2 rounded-[6px] cursor-pointer hover:bg-[#B71A1A] bg-[#E02424]"
                    >
                      <TrashCan class="size-5 text-neu-50" />
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Bagian Paginasi (Anda bisa mengembangkan ini nanti jika API Anda mendukung paginasi) -->
        <div class="flex justify-between items-center gap-3 flex-wrap mt-3">
          <div class="text-sm text-neu-600">
            Showing <span class="font-medium text-neu-900">1</span> to
            <span class="font-medium text-neu-900">{{ users.length }}</span> of
            <span class="font-medium text-neu-900">{{ users.length }}</span> Entries
          </div>
          <div class="flex items-center rounded-[8px] overflow-hidden">
            <div class="flex bg-neu-100 text-neu-300 gap-2 h-8 px-3 items-center font-semibold">
              <ArrowRight2Bold class="size-4 scale-x-[-1]" />Prev
            </div>
            <div class="flex bg-neu-100 gap-2 h-8 px-3 cursor-pointer items-center font-semibold">
              Next<ArrowRight2Bold class="size-4" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
