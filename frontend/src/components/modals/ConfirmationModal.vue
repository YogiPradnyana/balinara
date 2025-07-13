<script setup>
import { useModalStore } from '@/stores/modalStore';

const modalStore = useModalStore();

const handleConfirm = () => {
  if (typeof modalStore.onConfirm === 'function') {
    modalStore.onConfirm();
  }
  modalStore.closeModal();
};

const handleCancel = () => {
  if (typeof modalStore.onCancel === 'function') {
    modalStore.onCancel();
  }
  modalStore.closeModal();
};
</script>

<template>
  <transition
    enter-active-class="transition ease-out duration-200"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition ease-in duration-200"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <!-- ================================================================= -->
    <!-- PERUBAHAN UTAMA ADA DI BARIS INI -->
    <!-- Kelas 'bg-...' dihapus dan diganti dengan 'backdrop-blur-sm' -->
    <!-- ================================================================= -->
    <div v-if="modalStore.isOpen" class="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm" @click.self="handleCancel">
      <transition
        enter-active-class="transition ease-out duration-300"
        enter-from-class="opacity-0 scale-95"
        enter-to-class="opacity-100 scale-100"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-95"
      >
        <div class="bg-white rounded-2xl shadow-xl w-full max-w-md m-4 p-6">
          <div class="flex items-start gap-4">
            <!-- Ikon -->
            <div class="flex-shrink-0 flex items-center justify-center h-12 w-12 rounded-full bg-red-100">
              <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            </div>
            
            <div class="flex-grow">
              <h3 class="text-lg font-bold text-gray-900">{{ modalStore.title }}</h3>
              <p class="mt-2 text-sm text-gray-600">{{ modalStore.message }}</p>
            </div>
          </div>

          <div class="mt-6 flex justify-end gap-3">
            <button
              @click="handleCancel"
              type="button"
              class="px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 rounded-lg focus:outline-none"
            >
              Batal
            </button>
            <button
              @click="handleConfirm"
              type="button"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg focus:outline-none"
            >
              Ya, Hapus
            </button>
          </div>
        </div>
      </transition>
    </div>
  </transition>
</template>
