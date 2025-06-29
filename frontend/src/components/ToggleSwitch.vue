<script setup>
import { computed } from 'vue'

// Komponen ini menerima satu prop: `isActive` yang bertipe Boolean.
const props = defineProps({
  isActive: {
    type: Boolean,
    required: true,
  },
})

// Komponen ini akan memancarkan (emit) satu event bernama 'toggle'.
const emit = defineEmits(['toggle'])

// Fungsi yang akan dipanggil saat tombol diklik.
const toggle = () => {
  emit('toggle')
}

// Computed property untuk mengubah kelas CSS secara dinamis berdasarkan status `isActive`.
const backgroundClass = computed(() => (props.isActive ? 'bg-indigo-600' : 'bg-gray-200'))

const toggleClass = computed(() => (props.isActive ? 'translate-x-5' : 'translate-x-0'))

const iconClass = computed(() =>
  props.isActive ? 'opacity-100 duration-200 ease-in' : 'opacity-0 duration-100 ease-out',
)
</script>

<template>
  <button
    type="button"
    @click="toggle"
    :class="backgroundClass"
    class="relative inline-flex h-6 w-11 flex-shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-indigo-600 focus:ring-offset-2"
    role="switch"
    :aria-checked="isActive.toString()"
  >
    <span
      aria-hidden="true"
      :class="toggleClass"
      class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow-lg ring-0 transition duration-200 ease-in-out"
    >
    </span>
  </button>
</template>
