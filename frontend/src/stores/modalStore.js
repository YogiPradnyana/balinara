import { defineStore } from 'pinia';

export const useModalStore = defineStore('modal', {
  state: () => ({
    isOpen: false,
    title: '',
    message: '',
    onConfirm: null,
    onCancel: null,
  }),

  actions: {
    /**
     * Membuka modal dengan konfigurasi tertentu.
     * @param {object} config - Berisi title, message, dan fungsi onConfirm.
     */
    openModal({ title, message, onConfirm, onCancel = null }) {
      this.title = title;
      this.message = message;
      this.onConfirm = onConfirm; // Simpan fungsi yang akan dijalankan saat konfirmasi
      this.onCancel = onCancel;
      this.isOpen = true;
    },

    /**
     * Menutup modal dan mereset state.
     */
    closeModal() {
      this.isOpen = false;
      // Reset setelah modal tertutup agar tidak ada sisa state
      setTimeout(() => {
        this.title = '';
        this.message = '';
        this.onConfirm = null;
        this.onCancel = null;
      }, 300); // Sesuaikan dengan durasi transisi leave
    },
  },
});
