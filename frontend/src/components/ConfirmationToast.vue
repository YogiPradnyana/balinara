<script setup>
import { defineProps, defineEmits } from 'vue'

// Menerima fungsi sebagai props untuk dijalankan saat tombol diklik
const props = defineProps({
  message: String,
  onConfirm: Function,
  onCancel: Function,
})

// Mengirim event untuk menutup toast
const emit = defineEmits(['close'])

function handleConfirm() {
  props.onConfirm()
  emit('close') // Menutup toast setelah konfirmasi
}

function handleCancel() {
  props.onCancel()
  emit('close') // Menutup toast setelah batal
}
</script>

<template>
  <div class="flex flex-col items-start gap-2">
    <span>{{ message }}</span>
    <div class="flex gap-2 mt-2">
      <button
        @click="handleConfirm"
        class="px-3 py-1 text-sm font-semibold text-white bg-red-600 rounded hover:bg-red-700"
      >
        Ya, Hapus
      </button>
      <button
        @click="handleCancel"
        class="px-3 py-1 text-sm font-semibold bg-gray-200 rounded hover:bg-gray-300"
      >
        Batal
      </button>
    </div>
  </div>
</template>
