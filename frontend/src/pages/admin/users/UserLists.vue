<script setup>
import { onMounted, computed } from 'vue';
import { RouterLink } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { useUserStore } from '@/stores/userStore';     // <-- Gunakan userStore
import { useModalStore } from '@/stores/modalStore';   // <-- Gunakan modalStore

// Impor Ikon
import ArrowRight from '@/components/icons/ArrowRight.vue';
import ArrowRight2Bold from '@/components/icons/ArrowRight2Bold.vue';
import Edit from '@/components/icons/Edit.vue';
import Plus from '@/components/icons/Plus.vue';
import Search from '@/components/icons/Search.vue';
import Show from '@/components/icons/Show.vue';
import TrashCan from '@/components/icons/TrashCan.vue';

// Inisialisasi semua store
const authStore = useAuthStore();
const userStore = useUserStore();
const modalStore = useModalStore();

// ID user yang sedang login untuk perbandingan
const currentUserId = computed(() => authStore.currentUser?.id);

// Ambil data saat komponen dimuat
onMounted(() => {
  userStore.fetchUsers();
});

// Fungsi ini SEKARANG HANYA MEMBUKA MODAL
const confirmDelete = (user) => {
  modalStore.openModal({
    title: 'Konfirmasi Penghapusan',
    message: `Apakah Anda yakin ingin menghapus pengguna "${user.username}"? Tindakan ini tidak dapat dibatalkan.`,
    // Berikan fungsi yang akan dijalankan saat admin mengklik "Ya, Hapus"
    onConfirm: () => userStore.deleteUser(user.id) 
  });
};
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between gap-3 flex-wrap">
      <h1 class="text-3xl font-se font-semibold">Management</h1>
      <div class="flex gap-2 items-center text-sm font-medium">
        <span>Users</span> <ArrowRight class="size-4 text-neu-500" /> <span class="text-neu-500">Management</span>
      </div>
    </div>
    <div class="flex flex-col rounded-3xl border border-neu-100 p-4">
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
              <tr v-if="userStore.isLoading"><td colspan="6" class="p-4 text-center">Memuat data...</td></tr>
              <tr v-else-if="userStore.error"><td colspan="6" class="p-4 text-center text-red-500">{{ userStore.error }}</td></tr>
              <tr v-else-if="userStore.users.length === 0"><td colspan="6" class="p-4 text-center">Tidak ada data pengguna.</td></tr>
              <tr v-else v-for="(user, index) in userStore.users" :key="user.id" class="text-sm text-neu-700 border-b border-neu-100">
                <td class="p-4 text-neu-900">{{ (userStore.pagination.currentPage - 1) * 10 + index + 1 }}</td>
                <td class="p-4 text-neu-900 font-semibold">{{ user.username }}</td>
                <td class="p-4">{{ user.email }}</td>
                <td class="p-4">{{ user.phone || '-' }}</td>
                <td class="p-4">{{ user.is_staff ? 'Admin' : 'Traveler' }}</td>
                <td class="p-4 flex gap-3">
                  <!-- Tombol Edit: Aktif jika user adalah diri sendiri, nonaktif jika user lain -->
                  <RouterLink
                    v-if="user.id === currentUserId"
                    :to="{ name: 'AdminUserEdit', params: { id: user.id } }"
                    title="Edit" class="flex items-center justify-center p-2 rounded-md bg-[#FACA15] hover:bg-yellow-500">
                    <Edit class="size-5 text-neu-900" />
                  </RouterLink>
                  <button
                    v-else
                    title="Hanya bisa mengedit profil sendiri"
                    class="flex items-center justify-center p-2 rounded-md bg-gray-300 cursor-not-allowed"
                    disabled
                  >
                    <Edit class="size-5 text-gray-500" />
                  </button>

                  <!-- Tombol Detail -->
                  <RouterLink :to="{ name: 'AdminUserDetail', params: { id: user.id } }" title="Detail" class="flex items-center justify-center p-2 rounded-md bg-[#295F98] hover:bg-blue-800">
                    <Show class="size-5 text-white" />
                  </RouterLink>
                  
                  <!-- Tombol Hapus: Memanggil `confirmDelete` dan dinonaktifkan jika user adalah diri sendiri -->
                  <button 
                    @click="confirmDelete(user)" 
                    :disabled="user.id === currentUserId"
                    title="Delete" 
                    class="flex items-center justify-center p-2 rounded-md bg-[#E02424] hover:bg-red-700 disabled:bg-gray-300">
                    <TrashCan class="size-5 text-white" />
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
      <!-- Pagination -->
      <div class="flex justify-between items-center gap-3 flex-wrap mt-3" v-if="!userStore.isLoading && userStore.users.length > 0">
         <div class="text-sm text-neu-600">
            Showing {{ userStore.users.length }} of {{ userStore.pagination.count }} Entries
          </div>
          <div class="flex items-center rounded-lg overflow-hidden">
            <button :disabled="!userStore.pagination.previous" @click="userStore.fetchUsers(userStore.pagination.currentPage - 1)" class="flex items-center gap-2 h-8 px-3 font-semibold bg-neu-100 hover:bg-neu-200 disabled:text-neu-400">
              <ArrowRight2Bold class="size-4 scale-x-[-1]" />Prev
            </button>
            <button :disabled="!userStore.pagination.next" @click="userStore.fetchUsers(userStore.pagination.currentPage + 1)" class="flex items-center gap-2 h-8 px-3 font-semibold bg-neu-100 hover:bg-neu-200 disabled:text-neu-400 border-l border-neu-200">
              Next<ArrowRight2Bold class="size-4" />
            </button>
          </div>
      </div>
    </div>
  </div>
</template>
