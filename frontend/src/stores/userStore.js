import { defineStore } from 'pinia';
import userService from '@/services/userService';
import { showNotification } from '@/services/notificationService';

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [],
    pagination: {
      count: 0,
      next: null,
      previous: null,
      currentPage: 1,
    },
    isLoading: false,
    error: null,
  }),
  actions: {
    async fetchUsers(page = 1) {
      this.isLoading = true;
      this.error = null;
      try {
        const response = await userService.getAll({ page });
        this.users = response.data.results;
        this.pagination = {
          count: response.data.count,
          next: response.data.next,
          previous: response.data.previous,
          currentPage: page,
        };
      } catch (err) {
        this.error = 'Gagal memuat data pengguna.';
        console.error("Error fetching users:", err);
      } finally {
        this.isLoading = false;
      }
    },
    async deleteUser(userId) {
      try {
        await userService.deleteById(userId);
        showNotification('success', 'Pengguna berhasil dihapus.');
        // Ambil ulang data untuk memperbarui daftar di halaman saat ini
        await this.fetchUsers(this.pagination.currentPage);
      } catch (error) {
        showNotification('error', 'Gagal menghapus pengguna.');
        // Lemparkan error agar bisa ditangani jika perlu
        throw error;
      }
    },
  },
});
